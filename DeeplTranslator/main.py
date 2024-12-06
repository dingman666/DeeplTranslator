# -*- coding: utf-8 -*-
from wox import Wox, WoxAPI
import json
import httpx
import pyperclip

class DeepLXTranslator(Wox):
    
    # 语言映射表(支持中文名和代码)
    LANGUAGES = {
        'zh': '中文',
        'en': '英语',
        'ja': '日语',
        'ko': '韩语',
        'fr': '法语',
        'de': '德语',
        'es': '西班牙语',
        'it': '意大利语',
        'ru': '俄语',
        'pt': '葡萄牙语',
        'nl': '荷兰语',
        'pl': '波兰语',
        'tr': '土耳其语',
        'uk': '乌克兰语',
        # 可以继续添加更多语言...
    }

    def __init__(self):
        super().__init__()
        self.api_url = "https://deeplx.edu6.eu.org/translate?token=666666"

    def query(self, query):
        if not query.strip():
            return [{
                "Title": "DeepLX 翻译",
                "SubTitle": "用法: dl <目标语言> <文本> (例如: dl zh hello 或 dl 中文 hello)",
                "IcoPath": "Images\\icon.ico"
            }]

        parts = query.strip().split(maxsplit=1)

        # 处理语言搜索
        if len(parts) == 1:
            return self._search_languages(parts[0])

        # 处理翻译请求
        return self._handle_translation(parts[0], parts[1])

    def _search_languages(self, query):
        """模糊搜索语言"""
        query = query.lower()
        results = []
        
        for code, name in self.LANGUAGES.items():
            if (query in code.lower() or 
                query in name.lower() or 
                any(query in p for p in name)):
                
                results.append({
                    "Title": f"{name} ({code.upper()})",
                    "SubTitle": f"选择{name}作为目标语言",
                    "IcoPath": "Images\\icon.ico",
                    "JsonRPCAction": {
                        "method": "Wox.ChangeQuery",
                        "parameters": [f"dl {code} ", True],
                        "dontHideAfterAction": True
                    }
                })
        
        return results if results else [{
            "Title": "未找到匹配的语言",
            "SubTitle": "请检查语言输入是否正确",
            "IcoPath": "Images\\icon.ico"
        }]

    def _handle_translation(self, target_lang, text):
        """处理翻译请求"""
        try:
            # 统一转换语言代码
            target_lang = target_lang.lower()
            
            # 处理中文别名
            for code, name in self.LANGUAGES.items():
                if target_lang in name:
                    target_lang = code
                    break
            
            if target_lang not in self.LANGUAGES:
                return [{
                    "Title": "不支持的目标语言",
                    "SubTitle": "请输入正确的语言代码或名称",
                    "IcoPath": "Images\\icon.ico"
                }]

            # 准备翻译请求
            data = {
                "text": text,
                "source_lang": "auto",
                "target_lang": target_lang.upper()
            }
            
            # 发送请求
            response = httpx.post(
                url=self.api_url,
                data=json.dumps(data),
                timeout=10
            )
            
            result = response.json()
            translated_text = result['data']
            
            return [{
                "Title": translated_text,
                "SubTitle": f"原文: {text} | 目标语言: {self.LANGUAGES[target_lang]} | {len(text)}字符",
                "IcoPath": "Images\\icon.ico",
                "JsonRPCAction": {
                    "method": "copy_to_clipboard",
                    "parameters": [translated_text],
                    "dontHideAfterAction": False
                }
            }]

        except Exception as e:
            return [{
                "Title": "翻译失败",
                "SubTitle": f"错误信息: {str(e)}",
                "IcoPath": "Images\\icon.ico"
            }]

    def copy_to_clipboard(self, text):
        """复制到剪贴板并显示提示"""
        pyperclip.copy(text)
        WoxAPI.show_msg("已复制到剪贴板", text)

if __name__ == "__main__":
    DeepLXTranslator()