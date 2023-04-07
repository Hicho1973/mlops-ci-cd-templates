
import yaml
import os

def generate_ci_cd_workflow(repo_name, python_version='3.9', test_command='pytest', deploy_script='deploy.sh'):
    """
    Generates a GitHub Actions CI/CD workflow YAML for a Python project.

    This function creates a comprehensive GitHub Actions workflow that includes
    steps for linting, testing, building (Docker image), and deploying a Python application.
    It's designed to be easily customizable for different project needs.

    Args:
        repo_name (str): The name of the GitHub repository.
        python_version (str): The Python version to use for the workflow.
        test_command (str): The command to run for testing the application.
        deploy_script (str): The script to execute for deployment.

    Returns:
        dict: A dictionary representing the GitHub Actions workflow YAML.
    """
    workflow_content = {
        'name': 'Python CI/CD Pipeline',
        'on': {
            'push': {
                'branches': ['main', 'develop']
            },
            'pull_request': {
                'branches': ['main', 'develop']
            }
        },
        'jobs': {
            'build': {
                'runs-on': 'ubuntu-latest',
                'steps': [
                    {'uses': 'actions/checkout@v3'},
                    {
                        'name': 'Set up Python',
                        'uses': 'actions/setup-python@v3',
                        'with': {
                            'python-version': python_version
                        }
                    },
                    {
                        'name': 'Install dependencies',
                        'run': 'pip install --upgrade pip && pip install -r requirements.txt'
                    },
                    {
                        'name': 'Lint with flake8',
                        'run': 'pip install flake8 && flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics'
                    },
                    {
                        'name': 'Test with pytest',
                        'run': test_command
                    },
                    {
                        'name': 'Build Docker image',
                        'uses': 'docker/build-push-action@v2',
                        'with': {
                            'context': '.',  # Build context is the current directory
                            'push': False,   # Don't push in CI, only build
                            'tags': f'${{ github.repository }}:latest'
                        }
                    }
                ]
            },
            'deploy': {
                'runs-on': 'ubuntu-latest',
                'needs': 'build',
                'if': "github.ref == 'refs/heads/main'", # Deploy only on push to main
                'steps': [
                    {'uses': 'actions/checkout@v3'},
                    {
                        'name': 'Download Docker image',
                        'uses': 'docker/pull-action@v2',
                        'with': {
                            'repository': f'${{ github.repository }}',
                            'tag': 'latest'
                        }
                    },
                    {
                        'name': 'Deploy to production',
                        'env': {
                            'AWS_ACCESS_KEY_ID': '${{ secrets.AWS_ACCESS_KEY_ID }}',
                            'AWS_SECRET_ACCESS_KEY': '${{ secrets.AWS_SECRET_ACCESS_KEY }}'
                        },
                        'run': f'chmod +x {deploy_script} && ./{deploy_script}'
                    }
                ]
            }
        }
    }
    return workflow_content

def save_workflow_file(workflow_data, filename='python-ci-cd.yml', path='.github/workflows'):
    """
    Saves the generated workflow data to a YAML file.

    Args:
        workflow_data (dict): The workflow content as a dictionary.
        filename (str): The name of the YAML file.
        path (str): The directory where the file should be saved.
    """
    os.makedirs(path, exist_ok=True)
    filepath = os.path.join(path, filename)
    with open(filepath, 'w') as f:
        yaml.dump(workflow_data, f, sort_keys=False)
    print(f"GitHub Actions workflow saved to {filepath}")

if __name__ == '__main__':
    # Example usage:
    repo_name = os.getenv('GITHUB_REPOSITORY', 'Hicho1973/mlops-ci-cd-templates')
    workflow = generate_ci_cd_workflow(repo_name)
    save_workflow_file(workflow)

    # Create a dummy deploy script for demonstration
    deploy_script_content = """
#!/bin/bash

echo "Simulating deployment to production..."
echo "Deploying Docker image: ${{ github.repository }}:latest"
# Add actual deployment commands here, e.g., ECS deploy, Kubernetes apply, etc.
echo "Deployment successful!"
"""
    os.makedirs('scripts', exist_ok=True)
    with open('scripts/deploy.sh', 'w') as f:
        f.write(deploy_script_content)
    print("Dummy deploy.sh script created in scripts/deploy.sh")

    # Create a dummy test file
    test_file_content = """
import pytest

def test_example():
    assert 1 + 1 == 2

def test_another_example():
    assert "hello".upper() == "HELLO"
"""
    os.makedirs('tests', exist_ok=True)
    with open('tests/test_example.py', 'w') as f:
        f.write(test_file_content)
    print("Dummy test_example.py created in tests/test_example.py")

    # Create a dummy requirements.txt
    requirements_content = """
pytest
flake8
PyYAML
"""
    with open('requirements.txt', 'w') as f:
        f.write(requirements_content)
    print("Dummy requirements.txt created.")

    # Create a dummy main application file
    app_content = """
def main():
    print("Hello from the MLOps CI/CD template application!")

if __name__ == '__main__':
    main()
"""
    os.makedirs('app', exist_ok=True)
    with open('app/main.py', 'w') as f:
        f.write(app_content)
    print("Dummy app/main.py created.")
