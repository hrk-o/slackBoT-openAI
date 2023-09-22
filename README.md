# slackBoT-openAI

Lambda 環境変数  
BOT_TOKEN	xoxb-+++++-+++++  
OAUTH_TOKEN	xoxp-+++++-+++++  
OPENAI_KEY	sk-++++++++++
slackのBotとOpenAIのkeyを設定する  
  
API Gateway  
POST - 統合リクエストでLambda プロキシ統合の使用にチェック  

Slack Bot Token Scopes  
app_mentions:read　View messages that directly mention @chatGPT-BOT in conversations that the app is in  
chat:write　Send messages as @chatGPT-BOT  
