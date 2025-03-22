FROM python:3.12.1
RUN echo $PATH
RUN pip install poetry && export PATH="$PATH:/root/.local/bin"
RUN poetry --version
COPY . /src
WORKDIR /src
#RUN poetry cache clear --all
RUN poetry install -vvv
EXPOSE 8501
ENTRYPOINT ["poetry", "run", "streamlit", "run", "src/dataviz.py", "--server.port=8501", "--server.address=0.0.0.0"]