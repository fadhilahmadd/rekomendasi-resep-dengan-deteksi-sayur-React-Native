import React, { useState } from 'react';
import { View, Text, Button, Image, ScrollView, TouchableOpacity, Alert } from 'react-native';
import { ChevronLeftIcon, TrashIcon } from 'react-native-heroicons/outline';
import { widthPercentageToDP as wp, heightPercentageToDP as hp } from 'react-native-responsive-screen';
import { StatusBar } from 'expo-status-bar';
import { useNavigation } from '@react-navigation/native';
import * as ImagePicker from 'expo-image-picker';
import { CameraIcon, PhotoIcon } from 'react-native-heroicons/solid';

export default function UploadScreen() {
    const [selectedImages, setSelectedImages] = useState([]);
    const [uploadResponse, setUploadResponse] = useState(null);

    const navigation = useNavigation();

    const pickImages = async () => {
        const { status } = await ImagePicker.requestMediaLibraryPermissionsAsync();

        if (status !== 'granted') {
            Alert.alert('Peringatan', 'Permission to access media library is required!');
            return;
        }

        const result = await ImagePicker.launchImageLibraryAsync({
            mediaTypes: ImagePicker.MediaTypeOptions.All,
            allowsMultipleSelection: true,
            quality: 1,
        });

        if (result.cancelled) {
            return;
        }

        handleImageSelection(result.assets);
    };

    const captureFromCamera = async () => {
        const { status } = await ImagePicker.requestCameraPermissionsAsync();

        if (status !== 'granted') {
            Alert.alert('Peringatan', 'Permission untuk akses kamera dibutuhkan!');
            return;
        }

        const result = await ImagePicker.launchCameraAsync({
            mediaTypes: ImagePicker.MediaTypeOptions.Images,
            quality: 1,
        });

        if (result.cancelled) {
            return;
        }

        const uri = result.uri || (result.assets && result.assets.length > 0 && result.assets[0].uri);

        if (!uri) {
            // alert('Unable to get image URI from camera capture.');
            return;
        }

        handleImageSelection([{ ...result, name: uri.split('/').pop(), uri: uri }]);
    };

    const handleImageSelection = (images) => {
        const newImages = images.map((item) => {
            const fileType = item.uri.substring(item.uri.lastIndexOf('.') + 1);
            const mimeTypes = {
                jpg: 'image/jpeg',
                jpeg: 'image/jpeg',
                png: 'image/png',
                gif: 'image/gif',
            };
            const mimeType = mimeTypes[fileType.toLowerCase()] || 'application/octet-stream';

            return {
                uri: item.uri,
                name: item.fileName || item.uri.split('/').pop(),
                type: mimeType,
            };
        });

        setSelectedImages([...selectedImages, ...newImages]);
    };

    const uploadImages = async () => {
        if (!selectedImages || selectedImages.length <= 0) {
            Alert.alert('Peringatan', 'Tolong pilih gambar untuk upload.');
            return;
        }

        const data = new FormData();
        selectedImages.forEach((image, index) => {
            data.append('files[]', {
                uri: image.uri,
                name: image.name,
                type: image.type,
            });
        });

        try {
            const response = await fetch('http://192.168.0.160:5000/upload', {
                method: 'POST',
                body: data,
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            const result = await response.json();
            console.log(result);
            setUploadResponse(result);
        } catch (error) {
            console.error('Error uploading images:', error);
            setUploadResponse({ error: 'An error occurred while uploading images.' });
        }
    };

    const removeImage = (index) => {
        const updatedImages = [...selectedImages];
        updatedImages.splice(index, 1);
        setSelectedImages(updatedImages);
    };

    return (
        <ScrollView
            style={{ backgroundColor: '#FFFFFF' }}
            contentContainerStyle={{ paddingBottom: 30 }}
            showsVerticalScrollIndicator={false}
        >
            <StatusBar style='dark' />

            <View style={{ flexDirection: 'row', justifyContent: 'space-between', paddingTop: hp(5), paddingHorizontal: wp(5) }}>
                <TouchableOpacity onPress={() => navigation.navigate('Home')} style={{ padding: wp(2), borderRadius: 100, backgroundColor: 'white' }}>
                    <ChevronLeftIcon size={hp(3)} strokeWidth={4.5} color="#0891b2" />
                </TouchableOpacity>
            </View>

            <View style={{ paddingHorizontal: wp(4), marginTop: hp(5), justifyContent: 'space-between', flex: 1 }}>
                {selectedImages.length > 0 && (
                    <View style={{ marginBottom: hp(3) }}>
                        <Text style={{ fontSize: hp(2.5), fontWeight: 'bold', color: '#444444' }}>Gambar</Text>
                        <ScrollView horizontal showsHorizontalScrollIndicator={false} style={{ marginTop: hp(1) }}>
                            {selectedImages.map((image, index) => (
                                <View key={index} style={{ position: 'relative' }}>
                                    <Image source={{ uri: image.uri }} style={{ width: 100, height: 100, margin: 5 }} />
                                    <TouchableOpacity
                                        onPress={() => removeImage(index)}
                                        style={{ position: 'absolute', top: 5, right: 5 }}
                                    >
                                        <TrashIcon size={20} color="red" style={{backgroundColor: 'white'}}/>
                                    </TouchableOpacity>
                                </View>
                            ))}
                        </ScrollView>
                    </View>
                )}

                <View className="mb-1 flex-row justify-around">
                    <TouchableOpacity onPress={pickImages} className="" style={{ borderRadius: hp(2) }}>
                        <PhotoIcon size={hp(7)} strokeWidth={4.5} color="#0891b2" />
                        <Text style={{ fontSize: hp(1.6) }} className="text-neutral-700">Upload Gambar</Text>
                    </TouchableOpacity>
                    <TouchableOpacity onPress={captureFromCamera} className="" style={{ borderRadius: hp(2) }}>
                        <CameraIcon size={hp(7)} strokeWidth={4.5} color="#0891b2" />
                        <Text style={{ fontSize: hp(1.6) }} className="text-neutral-700">Ambil Gambar</Text>
                    </TouchableOpacity>
                    {/* <Button title="Pick Images" onPress={pickImages} /> */}
                </View>
                {/* <View className="mb-1">
                    <Button title="Capture from Camera" onPress={captureFromCamera} />
                </View> */}
                <View className="mb-1">
                    <Button title="Upload Images" onPress={uploadImages} />
                </View>

                {/* Display the upload response */}
                {uploadResponse && (
                    <View style={{ marginTop: 10 }}>
                        {uploadResponse.error ? (
                            <Text style={{ color: 'red' }}>{uploadResponse.error}</Text>
                        ) : (
                            <View>
                                <Text style={{ color: 'green' }}>Upload successful:</Text>
                                {uploadResponse.results && uploadResponse.results.length > 0 ? (
                                    <View>
                                        {uploadResponse.results.map((result, index) => (
                                            <Text key={index} style={{ color: 'green' }}>{index + 1}. {result.class}</Text>
                                        ))}
                                    </View>
                                ) : (
                                    <Text style={{ color: 'green' }}>No results found.</Text>
                                )}
                            </View>
                        )}
                    </View>
                )}
            </View>
        </ScrollView>
    );
}
