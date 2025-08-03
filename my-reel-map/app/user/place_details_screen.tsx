import React from 'react';
import { View, Text, StyleSheet, Button, Linking } from 'react-native';
import { useLocalSearchParams } from 'expo-router'; // or useRoute() if you're not using expo-router
import { IconSymbol } from '@/app-example/components/ui/IconSymbol.ios';

const PlaceDetailsScreen = () => {
  const {
    name,
    city,
    address_hint,
    type,
    summarize,
    google_maps_url,
    rating
  } = useLocalSearchParams();
  // Ensure all parameters are strings
  const placeDetails = {
    place_name: String(name || ''),
    place_city: String(city || ''),
    place_address_hint: String(address_hint || ''),
    place_type: String(type || ''),
    place_summarize: String(summarize || ''),
    place_google_maps_url: String(google_maps_url || ''),
    place_rating: String(rating || 'N/A')
  };
  return (
    <View style={styles.container}>
      <Text style={styles.title}>{placeDetails.place_name}</Text>
      <Text>City: {placeDetails.place_city}</Text>
      <Text>Address: {placeDetails.place_address_hint}</Text>
      <Text>Type: {placeDetails.place_type}</Text>
      <Text>Rating: {placeDetails.place_rating}</Text>
      <Text style={styles.summary}>{placeDetails.place_summarize}</Text>

      {placeDetails.place_google_maps_url && (
        <View style={styles.buttonWrapper}>
           <IconSymbol
            name="map"
            size={24}
            color="#000"
          />
          
          <Button
            title="Open in Google Maps"
            onPress={() => Linking.openURL(placeDetails.place_google_maps_url)}
          />
         
        </View>
      )}
  
    
    </View>
  );
};

export default PlaceDetailsScreen;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
    backgroundColor: '#fff',
    borderRadius: 8,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 2,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 8,
  },
  summary: {
    marginVertical: 12,
    fontStyle: 'italic',
  },
  buttonWrapper: {
    marginTop: 20,
  },

});
