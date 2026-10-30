pipeline {
    agent any
    triggers { pollSCM('H/2 * * * *') }
    environment { STORAGE = "${JENKINS_HOME}/storage/project" }
    stages {
        stage('Checkout master') {
            steps {
                git url: 'https://github.com/pavilk/jenkins-test.git', branch: 'master'
                sh 'rm -rf "$STORAGE" && mkdir -p "$(dirname "$STORAGE")" && cp -a . "$STORAGE"'
                sh 'ls -la "$STORAGE"'
            }
        }
    }
    post {
        success { build job: 'Job_2', wait: false }
    }
}
