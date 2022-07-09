import os
import pandas as pd

#load csv once it's created

class Question:
    '''
    DataFrames containing all questions as indices,
    and various properties of these questions as columns
    '''
    def __init__(self):
        # Assign an attribute ".data" to all new instances
        self.data = Olist().get_data()  #"Olist" will be replaced by the dataframe once the csv file is created

     def get_question(self):
        """
        Returns a DataFrame with:
        [questions]
        and filters out non-delivered orders unless specified
        """
        # Hint: Within this instance method, you have access to the instance of the class Question in the variable self, as well as all its attributes
        # make sure to create a copy rather than a "view"
        questions = self.data['questions'].copy()

class Response:
    '''
    DataFrames containing all orders as index,
    and various properties of these orders as columns
    '''
    def __init__(self):
        # Assign an attribute ".data" to all new instances
        self.data = Olist().get_data() #"Olist" will be replaced by the dataframe once the csv file is created

    def get_response(self):
        """
        Returns a DataFrame with:
        [responses]
        and filters out non-delivered orders unless specified
        """
        # Hint: Within this instance method, you have access to the instance of the class Question in the variable self, as well as all its attributes
        # make sure to create a copy rather than a "view"
        responses = self.data['responses'].copy()
