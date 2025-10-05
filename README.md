# Spark Data Analysis with Docker and Minikube

This repository demonstrates how to run a simple Spark data analysis job in two different containerized environments:

1.  A standalone Spark cluster using **Docker Compose**.
2.  A single-node Kubernetes cluster using **Minikube**.

The Spark application reads customer and transaction data from Parquet files and calculates the total amount spent by customers on "Entertainment" in 2018.

## Project Structure

```
.
├── app.py                  # The Python Spark application
├── data/                   # Directory for input Parquet files
│   ├── customers.parquet
│   └── transactions.parquet
├── docker-compose.yml      # Defines the Docker-based Spark cluster
├── Dockerfile              # Builds a custom image with our app and data
├── rbac.yaml               # K8s permissions for the Spark application
└── spark-submit-pod.yaml   # K8s pod to submit the Spark job
```

-----

## Part 1: Running with Docker Compose 🐳

This method creates a self-contained Spark cluster on your local machine with one master, two worker nodes, and a client to submit the job.

### Configuration

1.  **`app.py`**: Make sure the `SparkSession` is configured to connect to the Docker master node:
    ```python
    spark = SparkSession.builder \
        .appName("DataAnalysis") \
        .master("spark://spark-master:7077") \
        .getOrCreate()
    ```
2.  **`Dockerfile`**: Ensure the Dockerfile copies the application script:
    ```dockerfile
    FROM apache/spark:latest
    WORKDIR /app
    COPY app.py .
    ```
3.  **`docker-compose.yml`**: This file is pre-configured to build your image and orchestrate the cluster.

### Steps to Run

1.  **Build and Start the Cluster**: Open your terminal in the project root and run:

    ```sh
    docker-compose up --build
    ```

    This command will build the image for the `spark-submit` service, start all containers, and show you the logs.

2.  **Monitor the Cluster**: You can view the Spark Master's web UI by navigating to `http://localhost:8080` in your browser.

3.  **Shut Down**: Once the job is complete, you can stop and remove the containers:

    ```sh
    docker-compose down
    ```

-----

## Part 2: Running with Minikube (Kubernetes) 🚀

This method uses Minikube to create a single-node Kubernetes cluster and runs the Spark job on it.

### Configuration

1.  **`app.py`**: Comment out the Docker configuration and use the generic `SparkSession` builder. Kubernetes will handle the master URL automatically.
    ```python
    spark = SparkSession.builder.appName("DataAnalysis").getOrCreate()
    ```
2.  **`Dockerfile`**: Ensure the `Dockerfile` also copies your data files, as the Kubernetes pods will be self-contained.
    ```dockerfile
    FROM spark:latest
    WORKDIR /app
    COPY app.py .
    COPY data/ ./data/
    ```

### Steps to Run

1.  **Start Minikube**:

    ```sh
    minikube start
    ```

2.  **Set Docker Environment**: Point your local Docker client to Minikube's internal Docker registry. This is crucial so that the cluster can find your custom image.

    ```
    # For Linux/macOS
    # eval $(minikube -p minikube docker-env)
  
    # For Windows PowerShell
    minikube docker-env | Invoke-Expression
    ```

3.  **Build the Docker Image**: Build the image with a specific tag that matches the one in `spark-submit-pod.yaml`.

    ```sh
    docker build -t pyspark-app:latest .
    ```

4.  **Apply Permissions (RBAC)**: Apply the Role-Based Access Control rules to allow Spark to create and manage pods.

    ```sh
    kubectl apply -f rbac.yaml
    ```

5.  **Submit the Job**: Create the launcher pod, which will submit your application to the Kubernetes cluster.

    ```sh
    kubectl apply -f spark-submit-pod.yaml
    ```

6.  **Monitor the Job**: Check the status of your pods. You will see the `spark-submit-client` pod run and complete, followed by the creation of the `data-analysis-driver` and `data-analysis-exec` pods.

    ```sh
    kubectl get pods
    ```

7.  **View Logs**: To see the output of your script, view the logs of the driver pod.

    ```sh
    kubectl logs <your-driver-pod-name>
    ```

8.  **Clean Up**:

    ```sh
    # Stop the cluster
    minikube stop

    # Optional: Delete the cluster
    # minikube delete
    ```
