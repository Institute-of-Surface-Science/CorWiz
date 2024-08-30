import streamlit as st

st.title("Immersion Corrosion")

text_column, image_column = st.columns((0.7, 0.3))

with text_column:
    st.write("""
        ## What is Immersion Corrosion?

        Immersion corrosion refers to the deterioration of a material, typically a metal, when it is submerged in a corrosive liquid environment for an extended period. It is an electrochemical process that occurs when the metal is in direct contact with the electrolytic solution, leading to the formation of anodic and cathodic regions on the metal surface.

        ## Mechanism of Immersion Corrosion

        The mechanism of immersion corrosion involves the following steps:

        1. **Formation of an electrochemical cell**: When a metal is immersed in a corrosive solution, an electrochemical cell is formed, with the metal acting as the anode and the solution as the cathode.

        2. **Anodic and cathodic reactions**: At the anode, the metal undergoes oxidation, releasing electrons and forming metal ions. At the cathode, the reduction of dissolved oxygen or hydrogen ions occurs, consuming the electrons released at the anode.

        3. **Formation of corrosion products**: The metal ions react with other species in the solution, such as hydroxide ions or dissolved oxygen, to form insoluble corrosion products that deposit on the metal surface.

        ## Factors Affecting Immersion Corrosion

        Several factors can influence the rate and severity of immersion corrosion:

        1. **Composition of the corrosive solution**: The pH, temperature, and presence of dissolved ions or gases in the solution can affect the corrosion rate.

        2. **Velocity of the solution**: Higher solution velocities can increase the rate of mass transfer, leading to higher corrosion rates.

        3. **Surface characteristics of the metal**: The roughness, presence of defects, and microstructure of the metal surface can influence the corrosion rate.

        4. **Galvanic effects**: When dissimilar metals are in contact in the corrosive solution, galvanic corrosion can occur, accelerating the corrosion of the less noble metal.

        ## Mitigating Immersion Corrosion

        Several methods can be used to mitigate immersion corrosion, including:

        1. **Material selection**: Choosing corrosion-resistant materials, such as stainless steels or titanium alloys, can improve the resistance to immersion corrosion.

        2. **Coatings and linings**: Applying protective coatings or linings to the metal surface can create a barrier between the metal and the corrosive solution.

        3. **Cathodic protection**: This technique involves making the metal structure the cathode in an electrochemical cell, preventing the anodic dissolution of the metal.

        4. **Inhibitors**: Adding corrosion inhibitors to the solution can slow down the corrosion process by forming a protective film on the metal surface.

        In conclusion, immersion corrosion is a complex electrochemical process that occurs when metals are submerged in corrosive solutions. Understanding the mechanism and factors affecting immersion corrosion is crucial for developing effective prevention and mitigation strategies to ensure the longevity and reliability of metal components in immersion environments.

        Citations:
             
        [1] https://www.sciencedirect.com/science/article/pii/S2352492823010851
             
        [2] https://www.corrosionpedia.com/definition/2476/immersion-corrosion
             
        [3] https://www.corrosionpedia.com/definition/1243/immersion-test
             
        [4] https://www.mdpi.com/2075-4701/11/8/1317
             
        [5] https://www.sciencedirect.com/science/article/pii/S2238785423032222
             
        [6] https://www.db-thueringen.de/servlets/MCRFileNodeServlet/dbt_derivate_00051759/ilm1-2020000368.pdf
             
        [7] https://www.dreiym.com/2023/01/25/atmospheric-corrosion-what-it-is-and-how-to-mitigate-it/
             
        [8] https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5506901/
            
        [9] https://bluepapers.nl/index.php/bp/article/view/71
             
        [10] https://ieeexplore.ieee.org/document/8410876
    """)

with image_column:

    st.image('static/images/Metal-corrosion-in-underwater-cultural-heritage-Source-Pixabay-2016_W640.jpg', use_column_width=True)
    st.image('static/images/nterlink-between-natural-and-cultural-heritage-underwater-Source-Pixabay-2017_W640.jpg', use_column_width=True)
    st.image('static/images/Underwater-cultural-heritage-as-part-of-tourism-and-the-diving-industry-Source-Pixabay_W640.jpg', use_column_width=True)
    st.image('static/images/A-set-of-acquired-underwater-images-of-different-corrosion-patterens-arranged-per-degree_W640.jpg', use_column_width=True)

    st.markdown(
    '<div style="text-align: center;">Image credits [9], [10]</div>',
    unsafe_allow_html=True
    )   