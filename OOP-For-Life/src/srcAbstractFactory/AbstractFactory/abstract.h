#pragma once
#include "header.h"

enum eCars{
    PICKUP_TRUCK = 1,
    SPORTS = 2,
    CONVERTIBLE = 3
};

enum eVans{
    ASTRAZENECA = 1,
    NANOCOVAX = 2,
    PFIZER = 3
};

class Factory{
public:    
    static Cars* produceCars(eCars _carsID){
        switch (_carsID)
        {
          case 1: return new PickUpTruck();
          case 2: return new SportsCar();
          case 3: return new ConvertibleCar();
          default: return NULL;
        }
    }

    static sVehicles* produceVans(eVans _vansID){
        switch (_vansID)
        {
            case 1: return new AstraZenecaVan();
            case 2: return new NanoCovaxVan();
            case 3: return new PfizerVan(); 
            default: return NULL;
        }
    }
};