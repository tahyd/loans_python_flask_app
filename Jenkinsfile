def img
pipeline {
    environment {
        registry = "tahyd003/loans-app-flask"
        registryCredentials = "docker_id"
        githubCredentials = "tahyd"
        dockerImage = ""
        
    }
    agent any 
    
    stages {
        // Pull the code from GitHub
        stage("checkout"){
            steps {
              git branch: 'main',
              credentialsId: githubCredentials,
              url: 'https://github.com/tahyd/loans_python_flask_app.git'
            }
            
            }
            
         stage("Test"){
             
             steps {
                 echo "Testing completed"
             }
         }
         
         //  Clean the docker containers if already running
         stage ('Clean Up'){
            steps{
                sh returnStatus: true, script: 'docker stop $(docker ps -a | grep ${JOB_NAME} | awk \'{print $1}\')'
                sh returnStatus: true, script: 'docker rmi $(docker images | grep ${registry} | awk \'{print $3}\') --force' //this will delete all images
                sh returnStatus: true, script: 'docker rm ${JOB_NAME}'
            }
        }

       
         // Build docker image
         
        
        stage('Build Image') {
            steps {
                script {
                    img = registry + ":${env.BUILD_ID}"
                    println ("${img}")
                    dockerImage = docker.build("${img}")
                }
            }
        }
        
        // Push to docker hub
        
          stage('Push To DockerHub') {
            steps {
                script {
                    docker.withRegistry( 'https://registry.hub.docker.com ',registryCredentials ) {
                        dockerImage.push()
                    }
                }
            }
        }
        
        // Deploy in Local machine
        
        
        
         stage('Deploy') {
           steps {
                //sh label: '', script: "docker run -d --name ${JOB_NAME} -p 9090:9090 ${img}"
                echo 'abc'
               
          }
        }
        
        
        
    }
    
}