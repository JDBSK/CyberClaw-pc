import os
from typing import Any
from langchain_core.language_models.chat_models import BaseChatModel
from dotenv import load_dotenv
'''
多模型适配(Factory)
'''
load_dotenv()

def get_provider(
    provider_name: str = "openai", 
    model_name: str = "gpt-4o-mini", 
    temperature: float = 0.0,
    base_url: str | None = None,  # 【新增】允许外部传入 base_url
    api_key: str | None = None,   # 【新增】允许外部传入 api_key (可选)
    **kwargs: Any
) -> BaseChatModel:
    """
    模型适配器工厂。
    """
    provider_name = provider_name.lower()
    
    # 优先使用传入的 key，否则从环境变量获取
    current_api_key = api_key or os.environ.get("OPENAI_API_KEY")

    if provider_name == "openai":
 
        from langchain_openai import ChatOpenAI
        
        if not current_api_key:
            raise ValueError("未找到 OPENAI_API_KEY 环境变量！")
            
        return ChatOpenAI(
            model=model_name, 
            temperature=temperature,
            api_key=current_api_key,
            base_url=base_url,  # 如果为 None，则默认连接 api.openai.com
            **kwargs
        )

    elif provider_name == "aliyun" or provider_name == "dashscope":

        from langchain_openai import ChatOpenAI
        
        if not current_api_key:
            raise ValueError("未找到 API Key (请确保 .env 中配置了 OPENAI_API_KEY)")
            
        return ChatOpenAI(
            model=model_name, 
            temperature=temperature,
            api_key=current_api_key,
            base_url="https://coding.dashscope.aliyuncs.com/v1", 
            **kwargs
        )
        
    elif provider_name == "anthropic":
        from langchain_anthropic import ChatAnthropic
        key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not key:
            raise ValueError("未找到 ANTHROPIC_API_KEY 环境变量！")
            
        return ChatAnthropic(
            model_name=model_name, 
            temperature=temperature, 
            anthropic_api_key=key,
            **kwargs
        )
        
    elif provider_name == "ollama":
        from langchain_community.chat_models import ChatOllama
        return ChatOllama(
            model=model_name, 
            temperature=temperature, 
            base_url=kwargs.get("base_url", "http://localhost:11434"),
            **kwargs
        )
        
    else:
        raise ValueError(f"不支持的模型提供商: {provider_name}")

# 测试模型调用    
# LLM = get_provider(provider_name='aliyun', model_name='glm-5')
# res = LLM.invoke('你是谁')
# print(type(res))
# print(res)


