FROM amantiwari1/collegeapi:v0
WORKDIR /usr/src/app
COPY main.py main.py
EXPOSE 5000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]