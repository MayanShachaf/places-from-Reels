import React, { useState, useEffect } from "react";
import { View, Text, Button, FlatList, StyleSheet,Linking } from 'react-native';
import { useRouter } from "expo-router";
import { useLocalSearchParams } from "expo-router";
import { getUserPlaces,addFavoritePlace,get_favorite_places_ids} from "../../api/api"; // Adjust the import path as necessary
import { useFocusEffect } from '@react-navigation/native';
import { useCallback } from 'react';
import { FontAwesome } from '@expo/vector-icons';
import { TouchableOpacity } from 'react-native';

type Place = {
    place_id: string;
    name: string;
    city: string;
    address_hint: string;
    type: string;
    summarize: string;
    google_maps_url: string;
    rating: string; // Assuming rating is a string, adjust if necessary
    user_id: string;
};
const ScreenName = () => {
    const router = useRouter();
    const [showFavoritesOnly, setShowFavoritesOnly] = useState(false);
    const [loading, setLoading] = useState(false);
    const [favoritePlaceIds, setFavoritePlaceIds] = useState<string[]>([])
    const { id } = useLocalSearchParams();
    const userId = Array.isArray(id) ? id[0] : id ?? "";
  // State example
    const [placesList, setPlacesList] = useState<Place[]>([]);
  //  get all places 
  useFocusEffect(
    useCallback(() => {
      setLoading(true);
      get_favorite_places_ids(userId).then((placesIds) => {
  setFavoritePlaceIds(placesIds);
});
      getUserPlaces(userId)
        .then((places) => {
          const mergedPlaces = [
    ...places,
    {
      place_id: "1",
      name: "Example Place",
      city: "Example City",
      address_hint: "Example Address",
      type: "Example Type",
      summarize: "Example Summary",
      google_maps_url: "https://maps.example.com",
      user_id: userId,
      rating: "4.5" // Example rating
    },
  ];
  setPlacesList(mergedPlaces);
      })
        .finally(() => setLoading(false));
    }, [userId])
  );

  // Listen for new places added
 


  const handleAddReel = () => {
    // Example: validate or call API
    // router.push("/nextScreen");  // navigation
     router.push({
        pathname: "./add_reel_screen",
        params: { userId },
  });
}
  const handleFavoriteToggle = (placeId: string) => {
  if (!favoritePlaceIds.includes(placeId)) {
    setFavoritePlaceIds(prev => [...prev, placeId]); // Optimistically update UI
    addFavoritePlace(placeId, userId).catch(() => {
      // Revert if API fails
      setFavoritePlaceIds(prev => prev.filter(id => id !== placeId));
    });
  }
};
  

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Your places</Text>
      <Button title="add new reel" onPress={handleAddReel} />
      <Button
  title={showFavoritesOnly ? "Show All Places" : "Show My Favorites"}
  onPress={() => setShowFavoritesOnly(!showFavoritesOnly)}
/>
        {loading ? (<Text>Loading...</Text>
        ) : (
            <FlatList
                data={
    showFavoritesOnly
      ? placesList.filter((p) => favoritePlaceIds.includes(p.place_id))
      : placesList
  }
                keyExtractor={(item) => item.place_id}
                renderItem={({ item }) => (
                    <View style={styles.item}>
                        <Text>{item.name}</Text>
                        <Text>{item.city}</Text>
                        <Text>{item.address_hint}</Text>
                        <Text>{item.type}</Text>
                        <Text>{item.summarize}</Text>
                        <Text>{item.google_maps_url}</Text>
                        <Text>{item.rating}</Text>
                        {/* Only show button if URL exists */}
      {item.google_maps_url && (
        <Button
          title="Open in Google Maps"
          onPress={() => Linking.openURL(item.google_maps_url)}
        />
      )}
      <TouchableOpacity onPress={() => handleFavoriteToggle(item.place_id)}>
  <FontAwesome
    name={favoritePlaceIds.includes(item.place_id) ? "heart" : "heart-o"}
    size={20}
    color={favoritePlaceIds.includes(item.place_id) ? "red" : "gray"}
  />
</TouchableOpacity>
                    </View>
                )}
            />
            
        )}
    
  </View>
  );
};

export default ScreenName;

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
  },
  title: {
    fontSize: 22,
    marginBottom: 12,
  },
  item: {
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderColor: '#ccc',
  },
  buttonWrapper: {
    marginTop: 20,
  },
});

