FROM python:3.7

WORKDIR /topic_modelling_app

RUN /usr/local/bin/python -m pip install --upgrade pip

COPY requirements.txt requirements.txt 

RUN pip install -r requirements.txt 

EXPOSE 8501

COPY ./pages ./pages
COPY streamlit_app.py /topic_modelling_app

ENTRYPOINT [ "streamlit", "run" ]
CMD ["streamlit_app.py"]



COPY streamlit_app.py 

