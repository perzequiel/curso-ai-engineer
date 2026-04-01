class Rating: 
    REFERENCE_VALUE= 70
    def __init__(self, value: int | None = None):
        if value is not None and not isinstance(value, int): 
            raise TypeError("El valor de 'value' debe ser int o None")
        self.value = value
        
    def is_passing(self):
        return self.value is not None and self.value > self.REFERENCE_VALUE  
    
         













