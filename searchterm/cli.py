#!/usr/bin/env python3
"""
Command-line interface for searchterm AI chat application
"""

import click
import sys
from .model import Model
from .config_loader import (
    ConfigLoader,
    RED, YELLOW, GREEN, RESET
)


@click.group(invoke_without_command=True)
@click.argument('prompt', required=False)
@click.option('--max-tokens', type=int, help='Maximum tokens for response')
@click.option('--temp', type=float, help='Temperature for response (0.0-1.0)')
@click.option('--repeat-penalty', type=float, help='Repeat penalty for response (0.0-2.0)')
@click.option('--version', is_flag=True, help='Show version and exit')
@click.option('--settings', is_flag=True, help='Open interactive settings menu')
@click.pass_context
def main(ctx, prompt, max_tokens, temp, repeat_penalty, version, settings):
    """A simple command-line AI chat application."""
    
    config_loader = ConfigLoader()
    ctx.ensure_object(dict)
    ctx.obj['config_loader'] = config_loader
    
    if version:
        click.echo(f"searchterm version {config_loader.configvalues['VERSION']}")
        return
    
    if settings:
        config_loader = ConfigLoader()
        advanced_settings_menu(config_loader)
        return
    
    # no command is specified and we have prompt, run the chat
    if ctx.invoked_subcommand is None and prompt:
        click.echo(f"{RED}Error: No prompt provided. Use 'st --help' for usage.{RESET}")
        click.echo(f"{YELLOW}Tip: Use 'st settings' for configuration menu{RESET}")
        sys.exit(1)
        
        # reset to defaults if nothing given
        max_tokens = max_tokens or config_loader.configvalues["MAX_TOKENS"]
        temp = temp or config_loader.configvalues["TEMP"]
        repeat_penalty = repeat_penalty or config_loader.configvalues["REPEAT_PENALTY"]
        
        run_chat(prompt, max_tokens, temp, repeat_penalty)


def run_chat(prompt, max_tokens, temp, repeat_penalty):
    """Execute the chat functionality"""
    model = Model()
    curr_model = model.verify_model()
    
    if not curr_model:
        if click.confirm(f"{YELLOW}Model not found. Download {model.model_name}?{RESET}"):
            model.download_model()
            curr_model = model.verify_model()
            if not curr_model:
                click.echo(f"{RED}Model download failed. Exiting...{RESET}")
                sys.exit(1)
        else:
            click.echo(f"{RED}Model not found and download skipped. Exiting...{RESET}")
            sys.exit(1)

    try:
        with curr_model.chat_session():
            response = curr_model.generate(
                prompt=prompt, 
                max_tokens=max_tokens, 
                temp=temp, 
                repeat_penalty=repeat_penalty
            )
            click.echo(response)
    except Exception as e:
        click.echo(f"{RED}Error: {e}{RESET}")
        sys.exit(1)


def advanced_settings_menu(config_loader):
    """Advanced settings menu with better UX"""
    
    def show_menu():
        click.clear()
        click.echo(click.style("searchterm Settings", fg='cyan', bold=True))
        click.echo("-" * 40)
        click.echo()
        
        settings_display = [
            ("Model Name", config_loader.configvalues['MODEL'], 'green'),
            ("Max Tokens", config_loader.configvalues['MAX_TOKENS'], 'yellow'),
            ("Temperature", config_loader.configvalues['TEMP'], 'blue'),
            ("Repeat Penalty", config_loader.configvalues['REPEAT_PENALTY'], 'magenta'),
        ]
        
        for i, (name, value, color) in enumerate(settings_display, 1):
            click.echo(f"  {i}. {name}: {click.style(str(value), fg=color)}")
        
        click.echo()
        click.echo("Options:")
        click.echo("  r. Reset to defaults")
        click.echo("  s. Save and exit")
        click.echo("  q. Quit without saving")
        click.echo()
    
    modified_config = config_loader.configvalues.copy()
    
    while True:
        show_menu()
        
        try:
            choice = click.prompt(
                click.style("Select option", fg='yellow'),
                type=click.Choice(['1', '2', '3', '4', '5', 'r', 's', 'q']),
                show_choices=False
            )
            
            if choice == '1':
                new_value = click.prompt(
                    click.style("Model name", fg='green'),
                    default=modified_config['MODEL']
                )
                modified_config['MODEL'] = new_value
                
            elif choice == '2':
                new_value = click.prompt(
                    click.style("Max tokens", fg='yellow'),
                    type=click.IntRange(1, 4096),
                    default=modified_config['MAX_TOKENS']
                )
                modified_config['MAX_TOKENS'] = new_value
                
            elif choice == '3':
                new_value = click.prompt(
                    click.style("Temperature (0.0-2.0)", fg='blue'),
                    type=click.FloatRange(0.0, 2.0),
                    default=modified_config['TEMP']
                )
                modified_config['TEMP'] = new_value
                
            elif choice == '4':
                new_value = click.prompt(
                    click.style("Repeat penalty (0.0-2.0)", fg='magenta'),
                    type=click.FloatRange(0.0, 2.0),
                    default=modified_config['REPEAT_PENALTY']
                )
                modified_config['REPEAT_PENALTY'] = new_value
            
                
            elif choice == 'r':
                if click.confirm(click.style("Reset all settings to defaults?", fg='yellow')):
                    modified_config = config_loader.get_default_config()
                    click.echo(click.style("✓ Settings reset to defaults", fg='green'))
                    click.pause()
                    
            elif choice == 's':
                if config_loader.save_config(modified_config):
                    click.echo(click.style("✓ Settings saved successfully!", fg='green'))
                    click.echo("New Settings:")
                    for key, value in modified_config.items():
                        click.echo(f"  {key}: {click.style(str(value), fg='yellow')}")

                    click.pause(info='Press any key to exit...')
                    return
                else:
                    click.echo(click.style("✗ Failed to save settings", fg='red'))
                    click.pause()
                
            elif choice == 'q':
                if click.confirm(click.style("Exit without saving changes?", fg='red')):
                    return
                    
        except click.Abort:
            if click.confirm(click.style("Exit settings menu?", fg='red')):
                return


if __name__ == "__main__":
    main()