FROM amantiwari1/collegeapi:v0
WORKDIR /usr/src/app
RUN pip install pytest requests
COPY main.py main.py
COPY test_main.py test_main.py
RUN pytest
EXPOSE 5000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]