import streamlit as st

# IMPORT FUNCTIONS FROM UTILITIES FILE
from utlities import loadCachedData, lowercaseString

st.set_page_config(
    layout="wide",
)

st.title('Compare Lists')
st.subheader('')

# SET COLUMNS
col1, col2 = st.columns([1,2], gap="large")

# MAIN COLUMN OUTPUT
with col2:
    # DEFNINE EMPTY CONTAINER
    placeholder = st.empty()

# INIT BUTTON STATE
if "step_one_btn" not in st.session_state:
    st.session_state.step_one_btn = False

if "step_two_btn" not in st.session_state:
    st.session_state.step_two_btn = False

if "step_three_btn" not in st.session_state:
    st.session_state.step_three_btn = False

if "step_four_btn" not in st.session_state:
    st.session_state.step_four_btn = False

if "step_five_btn" not in st.session_state:
    st.session_state.step_five_btn = False


# BUTTON CALLBACK TO KEEP STEPS IN SHOWN STATE
# youtube.com/watch?v=XWKAtQIRyl
def callback(one,two,three,four,five):
    if (one):
        # step one btn was clicked!
        st.session_state.step_one_btn = True
    
    if (two):
        # step two btn was clicked!
        st.session_state.step_two_btn = True
    
    if (three):
        # step three btn was clicked!
        st.session_state.step_three_btn = True

    if (four):
        # step four btn was clicked!
        st.session_state.step_four_btn = True

    if (five):
        # step five btn was clicked!
        st.session_state.step_four_btn = True


# UPLOAD FILE
def uploadFile():
    # STEP #1
    col1.subheader('Step #1')
    # upload file
    main_file = col1.file_uploader("Main List (required)", type=['csv'], help='This is the file the records will edited.')
    everest_file = col1.file_uploader("Comparison List (required)", type=['csv'], help='This list is to check duplicates in column.')

    has_header = col1.checkbox('Does the comparision list have column headers?')
    delimitter = col1.selectbox('Delimiter', (',', '|'))
    upload_submit = col1.button('Upload',on_click=callback,args=(True,False,False,False,False))


    if (upload_submit or st.session_state.step_one_btn):
        if everest_file is not None and main_file is not None:
            readFile(everest_file,main_file,delimitter,has_header)
    
# READ FILE     
def readFile(everest_file,main_file,delimitter,has_header):
    if has_header:
        str_has_header = 'Yes'
    else:
        str_has_header = 'No'

    # READ FILE
    dataframe_everest = loadCachedData(everest_file,'',delimitter,str_has_header)
    dataframe_main_list = loadCachedData(main_file,'',delimitter,'Yes')    

    # STEP #2
    col1.divider()
    col1.header('Step #2')

    st.write(dataframe_everest)

    

    # GRAB EMAILS COLUMN

    if (has_header) :
        dataframe_comparision = col1.selectbox('Choose name of email column in comparison list. (optional)',  dataframe_everest.columns.ravel(),  help='Leave blank to look at first column.')
        if (dataframe_comparision):
            dataframe_valid_emails = dataframe_everest[dataframe_comparision].tolist() #Misc file with headers
    else:
        dataframe_valid_emails = dataframe_everest[dataframe_everest.columns[0]].tolist() #Everest

    #st.write(dataframe_valid_emails)

    # SELECTBOX FIELD
    emailColumn = col1.selectbox('Choose email column in main list.', dataframe_main_list.columns.ravel(),index=None)
    radio = col1.radio('How to compare?', ['Remove Duplicates','Keep Duplicates'], index=1)

    delete_invalid_submit = col1.button(label='Cleanse ›',on_click=callback,args=(True,True,False,False,False))

    if (delete_invalid_submit or st.session_state.step_two_btn) and emailColumn:
        dataframe_main_list = lowercaseString(dataframe_main_list,emailColumn)

        if radio == 'Keep Duplicates':
            scrubbed = dataframe_main_list[dataframe_main_list['emailaddress'].isin(dataframe_valid_emails)]
        else:
            scrubbed = dataframe_main_list[~dataframe_main_list['emailaddress'].isin(dataframe_valid_emails)]
        
        #placeholder.dataframe(scrubbed)


#INIT
uploadFile()


# df_CS_Sales_output[df_CS_Sales_output['emailaddress'].isin(CS_en_Sales_validated)]