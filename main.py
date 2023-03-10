import streamlit as st
import pandas as pd
from PIL import Image
import locale

cost_of_machine = 4650
image = Image.open('machine.png')


tab1, tab2 = st.tabs(["Basic Calculator", "Advanced Calculator"])


def basic_calculator():
    global labor_rate, standard_time_to_complete_job, cost_per_inch, average_inches_per_job, average_overweld, labor_effiecency, overweld_reduction, job_per_year, average_lifespan_of_machine
    st.title("")
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1: 
            labor_rate = st.number_input("Labor Rate:", value=25.00, step=.5, on_change=basic_on_change)
            average_inches_per_job = st.number_input("Average inches of weld per job:", value=1000, on_change=basic_on_change)
            average_overweld = st.slider("Average % of Overwelding", min_value=0, max_value=125, value=75, step=1, on_change=basic_on_change)
        with col2:
            job_per_year = st.number_input("Average number of jobs per year:", step=1, min_value=1, value=30, on_change=basic_on_change)
            cost_per_inch = st.number_input("Average cost per inch of weld:", value=1, on_change=basic_on_change)        
            labor_effiecency = st.slider("Average % increase of Labor Effieceny:",min_value=0, max_value=100, value=60, step=1, on_change=basic_on_change)        
        with col3:
            standard_time_to_complete_job = st.number_input("Average time to complete a job:", value=40, on_change=basic_on_change)
            average_lifespan_of_machine = st.number_input("Average lifespan of machine in years:", step=1, min_value=1, value=5, on_change=basic_on_change) 
            overweld_reduction = st.slider("Average % reduction in Overwelding:",min_value=0, max_value=100, value=50, step=1, on_change=basic_on_change)
    
    with st.container():
        column1, column2, column3 = st.columns(3)
        results = calculate_total_roi_over_lifespan(labor_rate, standard_time_to_complete_job, cost_per_inch, average_inches_per_job, average_overweld, labor_effiecency, overweld_reduction, job_per_year, average_lifespan_of_machine)

        with column1:
            formatted = "{:,.2f}".format(results['Lifespan ROI'])
            st.header("Total ROI")
            st.subheader('$ ' + str(formatted))
            
        with column2:
            formatted = "{:,.2f}".format(results['Yearly ROI']- cost_of_machine)
            st.header("Yearly ROI")
            st.subheader('$ ' + str(formatted))
            
        with column3:
            st.write("")
        
def advanced_calculator():   
    global total_labor_rate, average_inches_per_job, current_inch_per_minute, average_welder_efficiency, overweld_reduction, bill_rate
    with st.container():
        col1, col2, col3 = st.columns(3)
        with col1:
            total_labor_rate = st.number_input("Labor Rate (Including VOH):", value=25.00, step=.5, on_change=advanced_on_change)
            bill_rate = st.number_input("Bill Rate Per Hour:", value=125, step=1, on_change=advanced_on_change)
        with col2:
            average_inches_per_job = st.number_input("Inches Of Weld Per Job:", value=1000, on_change=advanced_on_change, step=1)
            average_welder_efficiency = st.slider("Average Welder Efficiency:",min_value=1, max_value=100, value=75, on_change=advanced_on_change, step=1)
            average_jobs = st.number_input("Average Number Of Jobs Per Year:", value=30, on_change=advanced_on_change, step=1)
        with col3:
            current_inch_per_minute = st.number_input("Optimal Welded Inches Per Minute:", value=20, on_change=advanced_on_change, step=1, min_value=1, max_value=30)
            overweld_reduction = st.slider("Average % Reduction in Overweld:",min_value=1, max_value=99, value=75, on_change=advanced_on_change, step=1)
            
    with st.container():
        column1, column2= st.columns(2)
        results = advanced_calculate(total_labor_rate, average_inches_per_job, current_inch_per_minute, average_welder_efficiency, overweld_reduction, bill_rate)
        with column1:
            job_formated = "{:.1f}".format(results['Overall Time Savings'] / 60)
            yearly_formated = "{:.1f}".format((results['Overall Time Savings'] / 60) * average_jobs)
            # st.header("Hours Saved Per Job:")
            st.subheader(str(job_formated + " hours saved per job."))
            st.subheader(str(yearly_formated + " hours saved per year."))
            
        with column2:
            job_formated = "{:,.0f}".format(results['$ Saved Per Job'])
            yearly_formated = "{:,.0f}".format(results['$ Saved Per Job'] * average_jobs)
            # st.header("$ Saved Per Job")
            st.subheader('$' + str(job_formated) + " saved per job.")
            st.subheader('$' + str(yearly_formated) + " saved per year.")
            
            
def advanced_on_change():
    advanced_calculate(total_labor_rate, average_inches_per_job, current_inch_per_minute, average_welder_efficiency, overweld_reduction, bill_rate)
    
def advanced_calculate(total_labor_rate, average_inches_per_job, current_inch_per_minute, average_welder_efficiency, overweld_reduction, bill_rate):
    output = {}
    output['Optimum Weld Time'] = (average_inches_per_job / current_inch_per_minute)
    output['Manual Weld Without Overweld'] = output['Optimum Weld Time'] / (average_welder_efficiency / 100)
    output['Manual Weld Without Overweld $'] = (output['Manual Weld Without Overweld'] * total_labor_rate) / 60
    output['Manual Weld With Overweld'] = output['Manual Weld Without Overweld'] / (1 - (overweld_reduction / 100))
    output['Manual Weld With Overweld $'] = (output['Manual Weld With Overweld'] * total_labor_rate) / 60
    output['Overall Time Savings'] = output['Manual Weld With Overweld'] - output['Optimum Weld Time']
    output['Time To Other Work'] = bill_rate * (output['Overall Time Savings'] / 60)
    output['$ Saved Per Job'] = output['Manual Weld With Overweld $'] - output['Manual Weld Without Overweld $']
    
    return output
    
    

def calculate_total_roi_over_lifespan(labor_rate, standard_time_to_complete_job, cost_per_inch, average_inches_per_job, average_overweld, labor_effiecency, overweld_reduction, job_per_year, average_lifespan_of_machine):  
    output = {}
    output['Total Welding Cost'] = (cost_per_inch * average_inches_per_job) * (1 + (average_overweld / 100))
    output['Total Labor Cost'] = labor_rate * standard_time_to_complete_job
    output['Labor Savings'] = output['Total Labor Cost'] * (labor_effiecency / 100)
    output['Optimal Welding Cost'] = ((cost_per_inch * average_inches_per_job)- output['Total Welding Cost']) * (overweld_reduction / 100)
    output['ROI Per Job'] = (output['Total Welding Cost']-output['Optimal Welding Cost']) + output['Labor Savings']
    output['Yearly ROI'] = output['ROI Per Job'] * job_per_year
    output['Lifespan ROI'] = (output['Yearly ROI'] * average_lifespan_of_machine) - cost_of_machine
    
    actual_output = pd.DataFrame(output, index=[0])
    
    return output

def basic_on_change():
    calculate_total_roi_over_lifespan(labor_rate, standard_time_to_complete_job, cost_per_inch, average_inches_per_job, average_overweld, labor_effiecency, overweld_reduction, job_per_year, average_lifespan_of_machine)


if __name__ == "__main__":
    with tab1:
        basic_calculator()
        
    with tab2:
        advanced_calculator()
