import streamlit as st
from header import add_header
from footer import add_footer

add_header()
st.title("Immersion Corrosion")

text_column, image_column = st.columns((0.7, 0.3))

with text_column:
    st.write("""
        ## What is Immersion Corrosion?

        **Immersion corrosion** refers to the deterioration of a material, typically metal, when it is submerged in a **corrosive liquid environment** for an extended period. This process is electrochemical in nature, occurring when the metal comes into direct contact with an electrolytic solution, leading to the formation of **anodic and cathodic regions** on the metal surface[2]. The result is often significant material degradation, which can compromise the integrity of submerged structures and components.

        ### The Mechanism of Immersion Corrosion

        The mechanism behind immersion corrosion is a complex sequence of electrochemical reactions:

        1. **Formation of an Electrochemical Cell**: When a metal is immersed in a corrosive solution, it acts as an anode while the surrounding solution functions as the cathode, forming an electrochemical cell[2][4][5].

        2. **Anodic and Cathodic Reactions**: At the anodic sites, the metal undergoes oxidation, releasing electrons and forming metal ions. Simultaneously, at the cathodic sites, reactions such as the reduction of dissolved oxygen or hydrogen ions occur, consuming the electrons released by the anodic process[2][4][5].

        3. **Formation of Corrosion Products**: The metal ions produced at the anode can react with other species in the solution, like hydroxide ions or dissolved oxygen, to form **insoluble corrosion products**. These products often deposit on the metal surface, potentially affecting further corrosion processes[2][4].

        ### Factors Influencing Immersion Corrosion

        The rate and severity of immersion corrosion are influenced by several factors:

        1. **Composition of the Corrosive Solution**: The **pH, temperature,** and the presence of dissolved ions or gases in the solution can significantly affect the corrosion rate[2][4].

        2. **Velocity of the Solution**: Higher solution velocities can increase the rate of mass transfer, leading to higher corrosion rates due to enhanced exposure to reactive species[2][4].

        3. **Surface Characteristics of the Metal**: The **roughness, presence of defects,** and microstructure of the metal surface play crucial roles in how the corrosion process develops[2][5].

        4. **Galvanic Effects**: When dissimilar metals are in contact within the corrosive solution, **galvanic corrosion** can occur, accelerating the corrosion of the less noble metal[2][5].

        ### Mitigating Immersion Corrosion

        Effective mitigation strategies are essential to prolong the lifespan of metals exposed to immersion environments. Common methods include:

        1. **Material Selection**: Opting for **corrosion-resistant materials**, such as stainless steels or titanium alloys, can greatly improve resistance to immersion corrosion[1][3][4].

        2. **Coatings and Linings**: Applying protective **coatings or linings** to the metal surface creates a barrier between the metal and the corrosive solution, thus preventing direct contact and subsequent corrosion[3][6].

        3. **Cathodic Protection**: By making the metal structure the cathode in an electrochemical cell, this technique prevents the anodic dissolution of the metal, effectively mitigating corrosion[3][5].

        4. **Inhibitors**: Adding **corrosion inhibitors** to the solution can slow down the corrosion process by forming a protective film on the metal surface[3][6].

        ### Conclusion

        Immersion corrosion is a complex and pervasive issue that can lead to significant material degradation in submerged environments. Understanding the underlying mechanisms and the factors that influence immersion corrosion is crucial for developing effective strategies to **prevent and mitigate** its effects. By doing so, industries can ensure the **longevity and reliability** of metal components in immersion environments.

        ### References

        [1] https://www.sciencedirect.com/science/article/pii/S2352492823010851  
        [2] https://www.corrosionpedia.com/definition/2476/immersion-corrosion  
        [3] https://www.corrosionpedia.com/definition/1243/immersion-test  
        [4] https://www.mdpi.com/2075-4701/11/8/1317  
        [5] https://www.sciencedirect.com/science/article/pii/S2238785423032222  
        [6] https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5506901/  
        [7] https://bluepapers.nl/index.php/bp/article/view/71  
        [8] https://ieeexplore.ieee.org/document/8410876
    """)

with image_column:

    st.image('static/images/Metal-corrosion-in-underwater-cultural-heritage-Source-Pixabay-2016_W640.jpg', caption="Image obtained from [7]", use_column_width=True) # incorrect attribution in source paper!
    st.image('static/images/nterlink-between-natural-and-cultural-heritage-underwater-Source-Pixabay-2017_W640.jpg', caption="Image obtained from [7]", use_column_width=True) # incorrect attribution in source paper!
    st.image('static/images/Underwater-cultural-heritage-as-part-of-tourism-and-the-diving-industry-Source-Pixabay_W640.jpg', caption="Image obtained from [7]", use_column_width=True) # incorrect attribution in source paper!
    st.image('static/images/A-set-of-acquired-underwater-images-of-different-corrosion-patterens-arranged-per-degree_W640.jpg', caption="Image obtained from [8]", use_column_width=True)  # correct citation


add_footer()