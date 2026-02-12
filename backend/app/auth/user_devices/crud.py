from app.common.base_crud import BaseCRUD
from app.auth.user_devices.models import UserDevice
from app.auth.user_devices.schemas import UserDeviceCreate, UserDeviceUpdate

class CRUDUserDevice(BaseCRUD[UserDevice, UserDeviceCreate, UserDeviceUpdate]):
    pass

user_device_crud = CRUDUserDevice(UserDevice)
