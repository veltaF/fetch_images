pipeline {
    agent any

    parameters {
        string(name: 'SITE_URL', defaultValue: "https://www.iana.org/help/example-domains", description: 'URL to fetch images from')
    }
    stages {
        stage('Cleanup') {
            steps {
                script {
                    cleanWs()
                }
            }
        }
        stage('Checkout') {
            steps {
                checkout([$class: 'GitSCM',
                          userRemoteConfigs: [[url: 'https://github.com/veltaF/fetch_images.git']],
                          branches: [[name: '*/main']]])
            }
        }
        stage('Setup Python Environment') {
            steps {
                script {
                    sh '''
                    python3 -m venv test_env
                    source test_env/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install . 
                    '''
                }
            }
        }
        stage('Run Tests') {
            steps {
                script {
                    sh """
                    source test_env/bin/activate
                    python3 -m unittest discover -s tests
                    """
                }
            }
        }
        stage('Run Python Tool') {
            steps {
                script {
                    sh """
                    source test_env/bin/activate
                    echo "SITE_URL: ${params.SITE_URL}"
                    fetch  ${params.SITE_URL}
                    """
                }
            }
        }
        stage('Compress Images') {
            steps {
                script {
                    sh 'zip -r downloaded_images.zip downloaded_images/'
                }
            }
        }
        stage('Archive Artifacts') {
            steps {
                script {
                    archiveArtifacts artifacts: 'downloaded_images.zip', allowEmptyArchive: true
                }
            }
        }
    }
}