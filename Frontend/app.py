import streamlit as st
import requests
import pandas as pd
import altair as alt

st.set_page_config(page_title="My Portfolio Dashboard",layout="wide")
st.title("My Portfolio")

# st.sidebar.title("Navigation")
tabs = st.tabs(["Dashboard","Skills"])

with tabs[0]:
    #DASHBOARD
    col1,col2 = st.columns([1,3])
    col1, col2 = st.columns([1, 3])

    with col1:
        st.image("image/profile.jpeg", width=300)
    
    with col2:
        st.markdown("""
        ### Hi, I'm Vishal 👋  

        Backend Developer with **1 year of professional experience** at **RGB Labs, Indian Institute of Technology Madras (IITM)**, building robust APIs and database-driven applications using **Python (Flask)** and **PostgreSQL**.  

        Passionate about **clean code** and **scalable backend systems**. Experienced in **agile environments** and cross-functional collaboration, including basic **UI design in Figma**.  

        Quick to adapt, continuously improving through **hands-on learning** and **new technologies**.  

        - 🏠 Based in: Chennai, India  
        - 💼 Role: Backend Developer  
        - 🎯 Goal: Aiming to build scalable products at top tech companies while solving real-world challenges.  
        - 📫 Reach me at: [LinkedIn](https://www.linkedin.com/in/vishal-m-9ab813263/) | [GitHub](https://github.com/settings/profile) | [Email](#)  
        """)

        st.markdown(f"""
                ### {"Experience"}
                -   Worked in 7+ unique backend projects ranging from internal tools to live production apps.
                -   Developed and deployed backend RESTful APIs using Python Flask for multiple internal tools and applications.
                -   Designed and managed relational database schemas and performed data manipulation using PostgreSQL with PgAdmin.
                -   Ensured API integration with frontend systems while maintaining performance and scalability.
                -   Collaborated with cross-functional teams and contributed to UI/UX discussions with basic Figma prototyping skills.
                """)
        
        st.markdown(f"""
                ### {"Language"}
                -  Tamil
                -  English
                -  Hindi
                """)
with tabs[1]:   
    #ANALYTICS OVERVIEW
    res = requests.get("http://127.0.0.1:5000/analytics/overview")

    if res.status_code == 200:
        overview = res.json()["details"]
        st.subheader("Overview")
        col1,col2,col3,col4 = st.columns(4)
        with col1:
            st.metric("Total Projects",overview["total_projects"])
        with col2:
            st.metric("Total Skills",overview["total_skills"])
        with col3:
            st.metric("Top Skill",overview["top_skill"])
        with col4:
            st.metric("Experience",overview["experience"])

    #ANALYTICS TREND

    res = requests.get("http://127.0.0.1:5000/analytics/trend")

    if res.status_code == 200:
        trend = res.json()

        st.subheader("Skills Highlight")
        col1,col2 = st.columns(2)
        
        with col1:
            for category, skills in trend["skills_highlight"].items():
                st.markdown(f"#### {category}")
                st.write(" | ".join([f"`{skill}`" for skill in skills]))

        with col2:
            st.subheader("Skills Distribution")
            df_dist = pd.DataFrame(trend["skills_distribution"])
            df_dist.index = df_dist.index + 1
            st.table(df_dist)

        
            # st.bar_chart(df_dist.set_index("category"))


    #PROJECTS

    res = requests.get("http://127.0.0.1:5000/get_projects")

    if res.status_code == 200:
        projects = res.json()["details"]
        df = pd.DataFrame(projects)
        df.index = df.index + 1
        st.subheader("Projects")

        for _, row in df.iterrows():
            st.markdown(f"""
            ### {row['project_name']}
            - ⏳ Duration: {row['duration_months']} months  
            - 📝 {row['description']}
            - 👨‍💻 Role: {row['role']}
            - ⚡ Tech: {row['tech_stack']}
            - 🔗 [GitHub]({row['github_link']})
            - 🎥 [Demo]({row['demo_link']})
            """)
            st.markdown("---")  
    
