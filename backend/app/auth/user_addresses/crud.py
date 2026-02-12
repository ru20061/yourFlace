from app.common.base_crud import BaseCRUD
from app.auth.user_addresses.models import UserAddress
from app.auth.user_addresses.schemas import UserAddressCreate, UserAddressUpdate

class CRUDUserAddress(BaseCRUD[UserAddress, UserAddressCreate, UserAddressUpdate]):
    pass

user_address_crud = CRUDUserAddress(UserAddress)
