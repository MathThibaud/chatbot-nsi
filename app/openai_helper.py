import openai

def get_openai_response(prompt):
    # Configurez votre clé API (à mettre dans les variables d'environnement)
    openai.api_key = os.getenv('OPENAI_API_KEY')
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message['content']
    except Exception as e:
        return f"Une erreur est survenue: {str(e)}"