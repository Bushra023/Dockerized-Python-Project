**Data Science Pipeline Project**  
This project demonstrates an end-to-end **Data Science workflow**, from database creation to data analysis and visualization, followed by containerization for scalability.  

**Overview**  
The primary goal of this project was to analyze a dataset, derive insights, and create visualizations, while ensuring portability through Docker.  

**Key Features**  
1. **Database Creation**:  
   - Built a relational database using **SQLite** to store and organize data efficiently.  
   - Structured the data with normalized tables for easy querying.  

2. **Data Analysis**:  
   - Queried the SQLite database using **SQLAlchemy** to extract and process data.  
   - Conducted exploratory data analysis (EDA) in Python to uncover trends and patterns.  

3. **Data Visualization**:  
   - Used Python libraries like **Matplotlib** and **Seaborn** to generate meaningful visualizations, including bar charts, line graphs, and scatter plots.  

4. **Containerization**:  
   - Containerized the entire project using **Docker** to ensure consistency across different environments.  
   - Created a Dockerfile and used Docker commands to build and run the image successfully.  

**Technologies Used**  
- **Database**: SQLite  
- **Programming Language**: Python (pandas, matplotlib, seaborn, SQLAlchemy)  
- **Containerization**: Docker  
- **Version Control**: Git  

**How to Run the Project**  
1. Clone the repository:  
   ```bash  
   git clone [repository-link]  
   ```  
2. Build the Docker image:  
   ```bash  
   docker build -t data-science-pipeline .  
   ```  
3. Run the Docker container:  
   ```bash  
   docker run -it data-science-pipeline  
   ```  

**Project Structure**  
- **data/**: Contains the dataset used in the project.  
- **scripts/**: Python scripts for querying and visualizations.  
- **Dockerfile**: Docker configuration file for containerization.  
- **README.md**: Project documentation.  
