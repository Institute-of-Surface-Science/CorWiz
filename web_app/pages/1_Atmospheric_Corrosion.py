import streamlit as st

st.title("Atmospheric Corrosion")

text_column, image_column = st.columns((0.7, 0.3))

with text_column:
    st.write("""
        ## What is Atmospheric Corrosion?

        Atmospheric corrosion is the deterioration of a material, typically a metal, due to its interaction with the surrounding atmosphere. It is an electrochemical process that requires the presence of an electrolyte, which is usually a thin film of moisture on the metal surface[1][2].

        ## Mechanism of Atmospheric Corrosion

        The mechanism of atmospheric corrosion involves the following steps:

        1. **Formation of an electrolyte layer**: When the relative humidity of the atmosphere exceeds a critical level (around 60% for iron in unpolluted atmospheres), a thin film of moisture forms on the metal surface[2].

        2. **Anodic and cathodic reactions**: In the presence of the electrolyte, atmospheric corrosion proceeds through anodic and cathodic reactions. The anodic reaction involves the dissolution of the metal, while the cathodic reaction is often the reduction of oxygen from the atmosphere[2].

        3. **Corrosion product formation**: The dissolved metal ions react with oxygen and water to form corrosion products, such as rust (iron oxide) on steel surfaces[1].

        ## Factors Affecting Atmospheric Corrosion

        Several factors influence the rate and severity of atmospheric corrosion:

        1. **Relative humidity**: Higher relative humidity increases the likelihood of moisture condensation on the metal surface, facilitating the formation of an electrolyte layer[1][2].

        2. **Temperature**: Increased temperature can accelerate the corrosion reactions and affect the properties of the electrolyte layer[1].

        3. **Atmospheric pollutants**: Pollutants like sulfur dioxide (SO2) and chlorides can increase the conductivity of the electrolyte layer, leading to higher corrosion rates[1][3].

        4. **Surface characteristics**: The roughness and cleanliness of the metal surface can influence the formation and properties of the electrolyte layer[5].

        ## Mitigating Atmospheric Corrosion

        Several methods are used to mitigate atmospheric corrosion, including:

        1. **Coatings and paints**: Applying protective coatings or paints to the metal surface can create a barrier between the metal and the atmosphere[3].

        2. **Cathodic protection**: This technique involves making the metal structure the cathode in an electrochemical cell, preventing the anodic dissolution of the metal[3].

        3. **Alloying and surface treatments**: Modifying the metal composition or surface properties can enhance its resistance to atmospheric corrosion[5].

        In conclusion, atmospheric corrosion is a complex electrochemical process that occurs when metals are exposed to the surrounding atmosphere. Understanding the mechanism and factors affecting atmospheric corrosion is crucial for developing effective prevention and mitigation strategies.

        Citations:
            
        [1] https://www.corrosionpedia.com/definition/116/atmospheric-corrosion
            
        [2] https://corrosion-doctors.org/AtmCorros/mechani1.htm
            
        [3] https://www.dreiym.com/2023/01/25/atmospheric-corrosion-what-it-is-and-how-to-mitigate-it/
            
        [4] https://www.diva-portal.org/smash/get/diva2:12811/FULLTEXT01.pdf
            
        [5] https://www.sciencedirect.com/science/article/pii/S2352492823010851
            
        [6] https://www.db-thueringen.de/servlets/MCRFileNodeServlet/dbt_derivate_00051759/ilm1-2020000368.pdf
            
        [7] https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5506901/
            
        [8] https://www.corrosionpedia.com/5-most-common-types-of-metal-coatings-that-everyone-should-know-about/2/6894
             
        [9] https://www.google.com/amp/s/www.azom.com/amp/article.aspx%3fArticleID=97
             
        [10] https://link.springer.com/chapter/10.1007/978-3-319-97625-9_12
             
        [11] https://www.google.com/amp/s/www.worldpipelines.com/business-news/13012017/sulzer-comments-on-corrosion-and-erosion/amp/
             
        [12] https://www.corrosionpedia.com/2/1525/corrosion/system-dependent-corrosion-in-piping-systems
    """)

with image_column:

    st.image('static/images/Atmospheric-corrosion-14_W640.jpg', use_column_width=True)
    st.image('static/images/Crevice-corrosion-17_W640.jpg', use_column_width=True)
    st.image('static/images/Erosion-corrosion-21_W640.jpg', use_column_width=True)
    st.image('static/images/Pitting-corrosion-18_W640.jpg', use_column_width=True)

    st.markdown(
    '<div style="text-align: center;">Image credits [9], [10], [11], [12]</div>',
    unsafe_allow_html=True
    )   