pipeline {
    agent any
    environment { STORAGE = "${JENKINS_HOME}/storage/project" }
    stages {
        stage('Push') {
            steps {
                dir(env.STORAGE) {
                    withCredentials([gitUsernamePassword(credentialsId: 'github')]) {
                        sh '''
                            git -c user.name=jenkins -c user.email=jenkins@localhost \
                                commit -m "Job_2: удалены trash1.txt и trash2.txt" || echo "нечего коммитить"
                            git push --force origin HEAD:jenkins-result
                        '''
                    }
                }
            }
        }
    }
}
