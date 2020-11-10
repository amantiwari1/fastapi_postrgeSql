FROM amantiwari1/collegeapi:latest
WORKDIR /usr/src/app
COPY main.py main.py
COPY test_main.py test_main.py
RUN pytest
EXPOSE 5000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]