from app.common.base_crud import BaseCRUD
from app.admin.faq.models import FAQ
from app.admin.faq.schemas import FAQCreate, FAQUpdate

class CRUDFAQ(BaseCRUD[FAQ, FAQCreate, FAQUpdate]):
    pass

faq_crud = CRUDFAQ(FAQ)
