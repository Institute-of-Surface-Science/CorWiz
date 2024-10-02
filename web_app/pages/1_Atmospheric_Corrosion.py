import streamlit as st

from header import add_header
from footer import add_footer

add_header()
st.title("Understanding Atmospheric Corrosion")

text_column, image_column = st.columns((0.7, 0.3))

with text_column:
    st.write("""
        ## Introduction to Atmospheric Corrosion

        **Atmospheric corrosion** is a common yet often underestimated process that affects various metals when exposed to the environment. Unlike corrosion that occurs in fully submerged conditions, atmospheric corrosion takes place on surfaces exposed to the air, where a thin film of moisture and pollutants interact with the metal. This process is particularly insidious because it can proceed slowly over time, causing significant damage before it becomes noticeable.

        ### The Process of Atmospheric Corrosion

        The onset of atmospheric corrosion begins when the **relative humidity** in the environment reaches a critical level—**around 60% for iron in unpolluted atmospheres**[2]. At this point, a thin layer of moisture condenses on the metal surface, forming an **electrolyte**. This electrolyte is essential for the electrochemical reactions that drive corrosion. On the metal's surface, **anodic reactions** cause the metal to dissolve, while **cathodic reactions** involve the reduction of oxygen from the air[2]. The metal ions produced during these reactions combine with oxygen and water to form corrosion products, such as **rust (iron oxide)** on steel, which accumulate on the surface[1].

        ### Factors Influencing Atmospheric Corrosion

        Atmospheric corrosion is influenced by several environmental and material factors:

        1. **Relative Humidity**: Elevated humidity levels increase moisture condensation on metal surfaces, facilitating corrosion[1][2].
        2. **Temperature**: Higher temperatures can accelerate the electrochemical reactions, potentially increasing the rate of corrosion[1].
        3. **Atmospheric Pollutants**: Airborne pollutants, such as sulfur dioxide (SO2) and chloride ions, enhance the corrosivity of the environment by increasing the conductivity of the electrolyte layer[1][3].
        4. **Surface Characteristics**: The texture and cleanliness of the metal surface play a crucial role in the formation and behavior of the electrolyte layer, affecting corrosion rates[4].

        ### Relevance and Applications

        Understanding atmospheric corrosion is vital across numerous industries, as it directly impacts the **durability and safety** of metallic structures. In the **infrastructure sector**, bridges, buildings, and other steel constructions are at constant risk of corrosion, which can lead to catastrophic failures if not properly managed. The **transportation industry** also faces significant challenges; vehicles, aircraft, and ships are routinely exposed to atmospheric conditions that can lead to corrosion, necessitating rigorous maintenance protocols to ensure their safe operation. In the **energy sector**, particularly in coastal areas, power plants and related equipment are exposed to harsh environmental conditions that promote corrosion. This can lead to efficiency losses and costly downtimes. Even in the **electronics industry**, where devices are often used in outdoor or varying atmospheric conditions, corrosion can compromise functionality and reliability.

        ### Strategies for Mitigating Atmospheric Corrosion

        To combat the effects of atmospheric corrosion, several strategies have been developed:

        1. **Protective Coatings**: Applying paints or other coatings creates a barrier that prevents the metal from direct exposure to the atmosphere[3].
        2. **Cathodic Protection**: This technique involves making the metal act as a cathode in an electrochemical cell, thereby preventing its dissolution[3].
        3. **Material Selection and Treatment**: Choosing **corrosion-resistant alloys** or applying surface treatments can significantly enhance the durability of metals exposed to the atmosphere[4].

        ### Conclusion

        Atmospheric corrosion is a complex and pervasive issue that affects a wide range of applications and industries. By understanding the mechanisms and factors that contribute to this type of corrosion, and by implementing effective prevention and mitigation strategies, it is possible to **protect valuable assets**, **reduce maintenance costs**, and **extend the life** of critical infrastructure.

        ### References

        [1] https://www.corrosionpedia.com/definition/116/atmospheric-corrosion  
        [2] https://corrosion-doctors.org/AtmCorros/mechani1.htm  
        [3] https://www.dreiym.com/2023/01/25/atmospheric-corrosion-what-it-is-and-how-to-mitigate-it/  
        [4] https://www.sciencedirect.com/science/article/pii/S2352492823010851  
        [5] https://www.corrosionpedia.com/2/1525/corrosion/system-dependent-corrosion-in-piping-systems  
        [6] https://www.azom.com/article.aspx?ArticleID=97
        [7] https://www.worldpipelines.com/business-news/13012017/sulzer-comments-on-corrosion-and-erosion/
    """)

with image_column:
    st.image('static/images/Atmospheric-corrosion-14_W640.jpg', caption="Image obtained from [5]", use_column_width=True) # correct citation
    st.image('static/images/Pitting-corrosion-18_W640.jpg', caption="Image obtained from [6]", use_column_width=True) # correct citation
    st.image('static/images/Erosion-corrosion-21_W640.jpg', caption="Image obtained from [7]", use_column_width=True) # correct citation


add_footer()