from app.config.db import async_session_maker

class SessionUow:
    def __init__(self) -> None:
        self.session_factory = async_session_maker
        
    async def __aenter__(self):
        self.session = self.session_factory()
        return self.session
    
    async def __aexit__(self, *args, **kwargs):
        await self.session.rollback()
        await self.session.close()