import { ref } from 'vue';
import { defineStore } from 'pinia';

const { VITE_KAKAO_MAP_KEY } = import.meta.env;

export const useMapStore = defineStore('kakaomap', () => {
  const scriptLoaded = ref(false);
  const places = ref([]);  // 검색된 장소
  const keyword = ref('');  // 검색어
  const isSearched = ref(false);  // 검색 상태
  let map = null;  // 지도 객체
  let markers = [];  // 지도에 추가된 마커들

  const loadKakaoMap = (container) => {
    if (!container) {
      console.error('지도를 표시할 컨테이너가 제공되지 않았습니다.');
      return;
    }

    if (scriptLoaded.value) {
      console.log('Kakao Maps 스크립트가 이미 로드되었습니다.');

      if (!map) {
        // 지도 객체가 초기화되지 않았으면 새로 초기화
        window.kakao.maps.load(() => {
          const mapOption = {
            center: new kakao.maps.LatLng(37.5657453, 126.9676032),
            level: 2,
          };
          map = new window.kakao.maps.Map(container, mapOption);
          const zoomControl = new kakao.maps.ZoomControl();
          map.addControl(zoomControl, kakao.maps.ControlPosition.RIGHT);

          // 이전 검색 결과와 마커 복원
          if (isSearched.value && places.value.length > 0) {
            places.value.forEach(place => {
              const lat = place.y;
              const lng = place.x;

              // 마커 추가
              const marker = new kakao.maps.Marker({
                position: new kakao.maps.LatLng(lat, lng),
                map: map,
              });
              markers.push(marker);

              // CustomOverlay 추가
              const content = `
                <div style="padding: 10px; background: white; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.2);">
                  <div style="margin: 0; font-size: 14px; word-break: keep-all; overflow-wrap: break-word;">
                    ${place.place_name}
                  </div>
                  <div style="margin: 5px 0 0 0; font-size: 12px; word-break: keep-all; overflow-wrap: break-word; color: #666;">
                    ${place.address_name}
                  </div>
                </div>
              `;
              const customOverlay = new kakao.maps.CustomOverlay({
                content: content,
                position: new kakao.maps.LatLng(lat, lng),
                yAnchor: 1.8,
              });
              customOverlay.setMap(map);
            });

            // 검색된 첫 번째 장소로 중심 위치 이동
            map.setCenter(new kakao.maps.LatLng(places.value[0].y, places.value[0].x));
          }
        });
      } else {
        console.log('지도가 이미 초기화되었습니다.');
      }
      return;
    }

    const script = document.createElement('script');
    script.src = `https://dapi.kakao.com/v2/maps/sdk.js?appkey=${VITE_KAKAO_MAP_KEY}&autoload=false&libraries=services`;
    document.head.appendChild(script);

    script.onload = () => {
      console.log('Kakao Maps 스크립트가 로드되었습니다.');
      scriptLoaded.value = true;
      window.kakao.maps.load(() => {
        const mapOption = {
          center: new kakao.maps.LatLng(37.5657453, 126.9676032),
          level: 2,
        };
        map = new window.kakao.maps.Map(container, mapOption);
        const zoomControl = new kakao.maps.ZoomControl();
        map.addControl(zoomControl, kakao.maps.ControlPosition.RIGHT);

        // 이전 검색 결과와 마커 복원
        if (isSearched.value && places.value.length > 0) {
          places.value.forEach(place => {
            const lat = place.y;
            const lng = place.x;

            // 마커 추가
            const marker = new kakao.maps.Marker({
              position: new kakao.maps.LatLng(lat, lng),
              map: map,
            });
            markers.push(marker);

            // CustomOverlay 추가
            const content = `
              <div style="padding: 10px; background: white; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.2);">
                <div style="margin: 0; font-size: 14px; word-break: keep-all; overflow-wrap: break-word;">
                  ${place.place_name}
                </div>
                <div style="margin: 5px 0 0 0; font-size: 12px; word-break: keep-all; overflow-wrap: break-word; color: #666;">
                  ${place.address_name}
                </div>
              </div>
            `;
            const customOverlay = new kakao.maps.CustomOverlay({
              content: content,
              position: new kakao.maps.LatLng(lat, lng),
              yAnchor: 1.8,
            });
            customOverlay.setMap(map);
          });

          // 검색된 첫 번째 장소로 중심 위치 이동
          map.setCenter(new kakao.maps.LatLng(places.value[0].y, places.value[0].x));
        }
      });
    };

    script.onerror = () => {
      console.error('Kakao Maps 스크립트를 로드하는 중 오류가 발생했습니다.');
    };
  };

  const searchPlaces = (query) => {
    if (!scriptLoaded.value || !map) {
      console.error('지도 또는 스크립트가 아직 로드되지 않았습니다.');
      return;
    }

    if (!query) {
      alert("검색어를 입력해주세요.");
      return;
    }

    // 기존 마커 제거
    markers.forEach(marker => marker.setMap(null));
    markers = [];

    keyword.value = `${query} 농협은행`;
    const ps = new kakao.maps.services.Places();

    ps.keywordSearch(keyword.value, (data, status) => {
      if (status === kakao.maps.services.Status.OK) {
        places.value = [...data.slice(0, 3)]; // 상위 3개만 선택
        isSearched.value = true;

        places.value.forEach((place) => {
          const lat = place.y;
          const lng = place.x;
        
          const marker = new kakao.maps.Marker({
            position: new kakao.maps.LatLng(lat, lng),
            map: map,
          });
          markers.push(marker);
        
          const content = `
            <div style="padding: 10px; background: white; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.2);">
              <div style="margin: 0; font-size: 14px; word-break: keep-all; overflow-wrap: break-word;">
                ${place.place_name}
              </div>
              <div style="margin: 5px 0 0 0; font-size: 12px; word-break: keep-all; overflow-wrap: break-word; color: #666;">
                ${place.address_name}
              </div>
            </div>
          `;
        
          // InfoWindow 대신 CustomOverlay 사용
          const customOverlay = new kakao.maps.CustomOverlay({
            content: content,
            position: new kakao.maps.LatLng(lat, lng),
            yAnchor: 1.8
          });
        
          customOverlay.setMap(map);
        });
        
        const firstPlace = places.value[0];
        map.setCenter(new kakao.maps.LatLng(firstPlace.y, firstPlace.x));
      } else {
        places.value = [];
        isSearched.value = true; // 검색은 수행되었음

        alert("검색된 결과가 없습니다.");
      }
    });
  };

  const setCenter = (place) => {
    if (!map) {
      console.error('지도가 초기화되지 않았습니다.');
      return;
    }
    map.setCenter(new kakao.maps.LatLng(place.y, place.x));
  };

  return { loadKakaoMap, searchPlaces, places, setCenter, isSearched };
});
