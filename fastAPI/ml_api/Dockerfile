#Base Image
FROM python:3.11-slim


#Set the working directory
WORKDIR /app

#Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

#Copy rest of the files
COPY . .

#Expose teh applicaiton port
EXPOSE 8000

#Command to start fastAPI application
CMD ["uvicorn","app:app","--host","0.0.0.0","--port","8000"]