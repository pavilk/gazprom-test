pipeline {
    agent any
    environment { STORAGE = "${JENKINS_HOME}/storage/project" }
    stages {
        stage('Remove files') {
            steps {
                dir(env.STORAGE) {
                    sh 'git rm --ignore-unmatch trash1.txt trash2.txt'
                    sh 'git status --short'
                }
            }
        }
    }
    post {
        success { build job: 'Job_3', wait: false }
    }
}
