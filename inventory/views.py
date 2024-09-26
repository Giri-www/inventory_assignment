from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.cache import cache
from .models import Item
from .serializers import ItemSerializer
from rest_framework.permissions import IsAuthenticated
import logging



logger = logging.getLogger(__name__)

""" Item Create API """
class ItemCreateView(APIView):
    """  # Require authentication for creating items """
    permission_classes = [IsAuthenticated] 

    def post(self, request):
        data = request.data
        logger.info(f""" The request data is => {data} """)
        item_name = data.get('name')
        
        """ Check if the item already exists """
        if Item.objects.filter(name=item_name).exists():
            return Response(
                {"error": "Item already exists."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        """ If item does not exist, create it """
        serializer = ItemSerializer(data=data)
        if serializer.is_valid():
            item_obj = serializer.save()
            cache_key = f"item_{item_obj.id}"
            cache.set(cache_key, serializer.data, timeout=60*15)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        """ Return error for invalid data """
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

""" Item Detail API """
class ItemDetailView(APIView):
    permission_classes = [IsAuthenticated] 

    def get(self, request, item_id):
        cache_key = f"item_{item_id}"
        logger.info(f"Cache key is {cache_key}")
        
        """ Check cache for the item """
        cached_item = cache.get(cache_key)
        if cached_item:
            logger.info(f"Returning cached item for ID {item_id}")
            return Response(cached_item, status=status.HTTP_200_OK)

        logger.info(f"The ID is {item_id}")

        """  get the item from the database  """
        try:
            item = Item.objects.get(id=item_id)
            logger.info(f"Item found: {item}")
        except Item.DoesNotExist:
            logger.error(f"Item with ID {item_id} not found.")
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        """ Serialize the item and store it in Redis ##"""
        serializer = ItemSerializer(item)
        cache.set(cache_key, serializer.data, timeout=60 * 15)  # Cache for 15 minutes

        logger.info(f"Serialized item data: {serializer.data}")
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, item_id):
        cache_key = f"item_{item_id}"
        logger.info(f"Updating item with ID {item_id}")
        
        """ To get the item from the database """
        try:
            item = Item.objects.get(id=item_id)
        except Item.DoesNotExist:
            logger.error(f"Item with ID {item_id} not found.")
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

        """ Update the item with the new data """
        serializer = ItemSerializer(item, data=request.data, partial=True)  
        if serializer.is_valid():
            serializer.save()
            """ Update cache after modifying the item == # Cache for 15 minutes #"""
            cache.set(cache_key, serializer.data, timeout= 60 * 15)  
            logger.info(f"Item updated successfully: {serializer.data}")
            return Response(serializer.data, status=status.HTTP_200_OK)

        logger.error(f"Failed to update item: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, item_id):
        cache_key = f"item_{item_id}"
        logger.info(f"Deleting item with ID {item_id}")
        
        """ Get the item from the database """
        try:
            item = Item.objects.get(id=item_id)
            item.delete()  
            logger.info(f"Item with ID {item_id} deleted successfully.")
            """ Remove the item from the cache """
            cache.delete(cache_key)
            return Response({"message": "Item deleted successfully."}, status=status.HTTP_200_OK)
        except Item.DoesNotExist:
            logger.error(f"Item with ID {item_id} not found.")
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)
