import openai
from .models import Conversation, Message, Context
import os

openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_response(conversation_id, user_message):
    conversation = Conversation.objects.get(id=conversation_id)
    context_data = {ctx.key: ctx.value for ctx in conversation.contexts.all()}
    
    # Generate response from OpenAI
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI expert providing advice."},
            *[{"role": msg.sender, "content": msg.content} for msg in conversation.messages.all()],
            {"role": "user", "content": user_message}
        ],
        context=context_data
    )
    
    ai_message = response.choices[0].message['content']
    
    # Save AI response and context
    Message.objects.create(conversation=conversation, sender='ai', content=ai_message)
    # Update context based on response or logic
    # Context.objects.update_or_create(conversation=conversation, key='key_name', defaults={'value': 'new_value'})
    
    return ai_message
