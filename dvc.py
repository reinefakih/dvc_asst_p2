# import statements
import subprocess # to run cmd commands
import argparse
# import os 
# CWD = os.getcwd()

# initialize dvc:
def initialize_dvc(working_directory: str):
    subprocess.call(['git', 'init'], cwd=working_directory) # initializing git repo
    subprocess.call(['dvc', 'init'], cwd=working_directory) # initializing dvc
    subprocess.call(['git', 'add', '.dvc', '.dvcignore'], cwd=working_directory) # adding just the dvc files to be tracked in git
    subprocess.call(['git', 'commit', '-m', '"initialized dvc"'], cwd=working_directory) # commiting with message to indicate that we initialized dvc


# adding a dataset to be tracked:
def add_file(file_name: str, directory_name: str, working_directory: str):
    subprocess.call(['dvc', 'add', f'{file_name}'], cwd=working_directory) # adding the dataset to dvc
    subprocess.call(['git', 'add', f'{directory_name}'], cwd=working_directory) # capturing the directory in git
    subprocess.call(['git', 'commit', '-m',f'"added initial version of {file_name}"'], cwd=working_directory) # commiting with message to show that we started versioning this dataset 


# commiting changes of already existing dataset:
def track_changes(file_name: str, message: str, working_directory: str):
    subprocess.call(['dvc', 'add', f'{file_name}'], cwd=working_directory) # running dvc add command to capture changes in already tracked dataset
    subprocess.call(['git', 'add', f'{file_name}.dvc'], cwd=working_directory) # captue changes of the .csv.dvc file
    subprocess.call(['git', 'commit', '-m', f'"{message}"'], cwd=working_directory) # commiting changes with a message


# seeing the status of our dataset (if they were modified for example):
def dvc_status(working_directory: str):
    subprocess.call(['dvc', 'status'], cwd=working_directory) # command to get the dvc status


# getting the commit history to see the hashes of the commits:
def git_log(working_directory: str):
    subprocess.call(['git', 'log', '--oneline'], cwd=working_directory) # command to get the commit hash with message line

# moving between versions
def go_back(hash_branch: str, working_directory: str):
    subprocess.call(['git', 'checkout', f'{hash_branch}'], cwd=working_directory) # go back to the version we want
    subprocess.call(['dvc', 'checkout'], cwd=working_directory) # revert the file to the version we wanted


# make changes to an old version of the data:
def make_changes_old(branch_name: str, file_name: str, directory_name: str, message: str, working_directory: str):
    subprocess.call(['git', 'switch', '-c', f'{branch_name}'], cwd=working_directory) # make a new branch to save changes of an old version
    subprocess.call(['dvc', 'add', f'{file_name}'], cwd=working_directory) # capture changes of the dataset
    subprocess.call(['git', 'add', f'{directory_name}'], cwd=working_directory) # stage changes in the directory
    subprocess.call(['git', 'commit', '-m', f'{message}'], cwd=working_directory) # commit changes with a message

def main():
    parser = argparse.ArgumentParser(description="DVC and Git automation script")
    
    subparsers = parser.add_subparsers(dest='command')

    # Subparser for initialize_dvc
    initialize_dvc_parser = subparsers.add_parser('initialize_dvc', help='Initialize DVC and Git in the main directory')
    initialize_dvc_parser.add_argument('--working_directory', required=True, type=str, help='Directory to run the command on')

    # Subparser for add_file
    add_file_parser = subparsers.add_parser('add_file', help='Add a file to DVC tracking')
    add_file_parser.add_argument('--file_name', required=True, type=str, help='Name of the file to be added')
    add_file_parser.add_argument('--directory_name', required=True, type=str, help='Name of the directory where the file is located')
    add_file_parser.add_argument('--working_directory', required=True, type=str, help='Directory to run the command on')

    # Subparser for track_changes
    track_changes_parser = subparsers.add_parser('track_changes', help='Track changes of an existing dataset')
    track_changes_parser.add_argument('--file_name', required=True, type=str, help='Name of the file to track changes')
    track_changes_parser.add_argument('--message', required=True, type=str, help='Commit message for tracking changes')
    track_changes_parser.add_argument('--working_directory', required=True, type=str, help='Directory to run the command on')

    # Subparser for dvc_status
    dvc_status_parser = subparsers.add_parser('dvc_status', help='Check the status of DVC tracked files')
    dvc_status_parser.add_argument('--working_directory', required=True, type=str, help='Directory to run the command on')

    # Subparser for git_log
    gitlog_parser = subparsers.add_parser('git_log', help='Get the commit history')
    gitlog_parser.add_argument('--working_directory', required=True, type=str, help='Directory to run the command on')

    # Subparser for go_back
    go_back_parser = subparsers.add_parser('go_back', help='Go back to a specific version')
    go_back_parser.add_argument('--hash_branch', required=True, type=str, help='Hash or branch name to checkout')
    go_back_parser.add_argument('--working_directory', required=True, type=str, help='Directory to run the command on')

    # Subparser for make_changes_old
    make_changes_old_parser = subparsers.add_parser('make_changes_old', help='Make changes to an old version of the data')
    make_changes_old_parser.add_argument('--branch_name', required=True, type=str, help="Name of the new branch")
    make_changes_old_parser.add_argument('--file_name', required=True, type=str, help="Name of the modified file")
    make_changes_old_parser.add_argument('--directory_name', required=True, type=str, help="Directory name where the data is stored")
    make_changes_old_parser.add_argument('--message', required=True, type=str, help='Commit message')
    make_changes_old_parser.add_argument('--working_directory', required=True, type=str, help='Directory to run the command on')

    args = parser.parse_args()
    
    if args.command == 'initialize_dvc':
        initialize_dvc(args.working_directory)
    elif args.command == 'add_file':
        add_file(args.file_name, args.directory_name, args.working_directory)
    elif args.command == 'track_changes':
        track_changes(args.file_name, args.message, args.working_directory)
    elif args.command == 'dvc_status':
        dvc_status(args.working_directory)
    elif args.command == 'git_log':
        git_log(args.working_directory)
    elif args.command == 'go_back':
        go_back(args.hash_branch, args.working_directory)
    elif args.command == 'make_changes_old':
        make_changes_old(args.branch_name, args.file_name, args.directory_name, args.message, args.working_directory)

if __name__ == '__main__':
    main()
