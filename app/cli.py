"""
Command-line interface for local agent interactions.

This module provides a CLI for interacting with the local agents.
"""

import argparse
import sys
from typing import Optional

try:
    from app.agents import get_strategy_agent, get_coding_agent
    from app.main import revamp_project, revamp_and_implement
except ImportError:
    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from app.agents import get_strategy_agent, get_coding_agent
    from app.main import revamp_project, revamp_and_implement


def strategy_command(args):
    """Run strategy agent."""
    agent = get_strategy_agent()
    
    if args.interactive:
        print("🤖 Strategy Agent - Interactive Mode")
        print("=" * 50)
        print("Enter your query (or 'exit' to quit):")
        
        while True:
            try:
                query = input("\n> ")
                if query.lower() in ['exit', 'quit', 'q']:
                    break
                
                if query.strip():
                    response = agent.run(query)
                    print("\n" + response.content)
            except KeyboardInterrupt:
                print("\n\nExiting...")
                break
    else:
        if not args.query:
            print("Error: --query is required in non-interactive mode")
            sys.exit(1)
        
        response = agent.run(args.query)
        print(response.content)


def coding_command(args):
    """Run coding agent."""
    agent = get_coding_agent()
    
    if args.interactive:
        print("💻 Coding Agent - Interactive Mode")
        print("=" * 50)
        print("Enter your coding task (or 'exit' to quit):")
        
        while True:
            try:
                query = input("\n> ")
                if query.lower() in ['exit', 'quit', 'q']:
                    break
                
                if query.strip():
                    response = agent.run(query)
                    print("\n" + response.content)
            except KeyboardInterrupt:
                print("\n\nExiting...")
                break
    else:
        if not args.query:
            print("Error: --query is required in non-interactive mode")
            sys.exit(1)
        
        response = agent.run(args.query)
        print(response.content)


def revamp_command(args):
    """Run revamp workflow."""
    result = revamp_project(
        github_url=args.github_url,
        hackathon_url=args.hackathon_url,
        hackathon_context=args.context,
        search_order=args.search_order,
        search_topic=args.topic
    )
    print(result)


def implement_command(args):
    """Run revamp and implementation workflow."""
    result = revamp_and_implement(
        github_url=args.github_url,
        hackathon_url=args.hackathon_url,
        hackathon_context=args.context,
        search_order=args.search_order,
        search_topic=args.topic,
        implement_changes=args.implement,
        fork_repo=args.fork,
        branch_name=args.branch
    )
    
    print("\n" + "=" * 50)
    print("STRATEGY")
    print("=" * 50)
    print(result["strategy"])
    
    if result["implementation"]:
        print("\n" + "=" * 50)
        print("IMPLEMENTATION")
        print("=" * 50)
        print(result["implementation"])


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Hackathon Project Revamp Agent - Local CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive strategy agent
  python -m app.cli strategy --interactive

  # Run strategy query
  python -m app.cli strategy --query "Analyze this project: https://github.com/user/repo"

  # Revamp project
  python -m app.cli revamp --github-url https://github.com/user/repo --hackathon-url https://hackathon.com

  # Full workflow with implementation
  python -m app.cli implement --github-url https://github.com/user/repo --implement --fork
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to run')
    
    # Strategy agent command
    strategy_parser = subparsers.add_parser('strategy', help='Run strategy agent')
    strategy_parser.add_argument('--query', '-q', help='Query to run')
    strategy_parser.add_argument('--interactive', '-i', action='store_true', help='Interactive mode')
    strategy_parser.set_defaults(func=strategy_command)
    
    # Coding agent command
    coding_parser = subparsers.add_parser('coding', help='Run coding agent')
    coding_parser.add_argument('--query', '-q', help='Query to run')
    coding_parser.add_argument('--interactive', '-i', action='store_true', help='Interactive mode')
    coding_parser.set_defaults(func=coding_command)
    
    # Revamp command
    revamp_parser = subparsers.add_parser('revamp', help='Generate revamp strategy')
    revamp_parser.add_argument('--github-url', help='GitHub repository URL')
    revamp_parser.add_argument('--hackathon-url', help='Hackathon website URL')
    revamp_parser.add_argument('--context', help='Additional hackathon context')
    revamp_parser.add_argument('--search-order', choices=['projects_first', 'hackathons_first'], 
                              default='projects_first', help='Search order for discovery')
    revamp_parser.add_argument('--topic', help='Search topic for discovery')
    revamp_parser.set_defaults(func=revamp_command)
    
    # Implement command
    implement_parser = subparsers.add_parser('implement', help='Generate strategy and implement')
    implement_parser.add_argument('--github-url', help='GitHub repository URL')
    implement_parser.add_argument('--hackathon-url', help='Hackathon website URL')
    implement_parser.add_argument('--context', help='Additional hackathon context')
    implement_parser.add_argument('--search-order', choices=['projects_first', 'hackathons_first'], 
                                 default='projects_first', help='Search order for discovery')
    implement_parser.add_argument('--topic', help='Search topic for discovery')
    implement_parser.add_argument('--implement', action='store_true', help='Enable code implementation')
    implement_parser.add_argument('--fork', action='store_true', help='Fork repository before implementing')
    implement_parser.add_argument('--branch', default='hackathon-revamp', help='Branch name for changes')
    implement_parser.set_defaults(func=implement_command)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == "__main__":
    main()