How to Run the Project 
Follow these simple steps to set up and run the project on your machine: 

Prerequisites 
   - Ensure you have Git Bash, PowerShell, or a terminal installed on your system. 
   - Install Docker and Docker Compose: 
   - Download and install Docker from https://www.docker.com/. 
   - Ensure Docker is running before proceeding. 

   - Install Visual Studio Code (VS Code) if you plan to use it:  
   - Download and install VS Code from https://code.visualstudio.com/. 

Steps to Run the Project 
   - Extract the Project Files: 
   - Locate the provided zip file and extract its contents to a folder on your system. 

   Option 1: Using the Terminal 
      - Open your terminal (Git Bash, PowerShell, or any terminal of your choice). 
      - Use the cd command to change into the directory where the project was extracted. For example: cd /path/to/extracted-folder 
      
   Option 2: Using Visual Studio Code 
      - Open VS Code on your machine. 
      - Drag and drop the extracted project folder into the VS Code editor. 
      - Open the built-in terminal in VS Code by navigating to View > Terminal or pressing Ctrl + ~. 
      - Use the terminal to navigate to the project folder if it isn't already selected: cd /path/to/extracted-folder 
      
   Run the Application: 
   - Start the application by running the following command in your terminal: docker-compose up 
      
   If you encounter any issues, ensure Docker is installed and running. 

   Access the API Documentation: 
      - Once the application is running, open your web browser and navigate to: http://localhost:8000/docs 
      - This will open the API documentation where you can experiment with the endpoints. 

That's It! 
The application is now up and running. Whether you're using VS Code or your terminal, you can now enjoy exploring the API. Have fun! 