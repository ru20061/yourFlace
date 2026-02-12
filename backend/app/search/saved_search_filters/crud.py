from app.common.base_crud import BaseCRUD
from app.search.saved_search_filters.models import SavedSearchFilter
from app.search.saved_search_filters.schemas import SavedSearchFilterCreate, SavedSearchFilterUpdate

class CRUDSavedSearchFilter(BaseCRUD[SavedSearchFilter, SavedSearchFilterCreate, SavedSearchFilterUpdate]):
    pass

saved_search_filter_crud = CRUDSavedSearchFilter(SavedSearchFilter)
