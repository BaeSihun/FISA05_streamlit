import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# 클러스터링 관련 함수들
def calculate_scores(data):
    """각 차량에 대해 3파트별 점수 계산"""
    # 속도 점수 (최고속도 70% + 가속성능 30%)
    speed_score = (
        (data['top_speed_kmh'] / data['top_speed_kmh'].max()) * 0.7 +
        ((data['acceleration_0_100_s'].max() - data['acceleration_0_100_s']) / 
         (data['acceleration_0_100_s'].max() - data['acceleration_0_100_s'].min())) * 0.3
    ) * 100
    
    # 배터리 성능 점수 (배터리용량 40% + 주행거리 40% + 효율성 20%)
    battery_score = (
        (data['battery_capacity_kWh'] / data['battery_capacity_kWh'].max()) * 0.4 +
        (data['range_km'] / data['range_km'].max()) * 0.4 +
        ((data['efficiency_wh_per_km'].max() - data['efficiency_wh_per_km']) / 
         (data['efficiency_wh_per_km'].max() - data['efficiency_wh_per_km'].min())) * 0.2
    ) * 100
    
    # 충전 속도 점수 (급속충전출력 80% + 배터리용량 20%)
    charging_score = (
        (data['fast_charging_power_kw_dc'] / data['fast_charging_power_kw_dc'].max()) * 0.8 +
        (data['battery_capacity_kWh'] / data['battery_capacity_kWh'].max()) * 0.2
    ) * 100
    
    return speed_score, battery_score, charging_score

def assign_clusters(data):
    """백분위 기반 클러스터 분류"""
    speed_cutoff = np.percentile(data['speed_score'], 67)
    battery_cutoff = np.percentile(data['battery_score'], 67) 
    charging_cutoff = np.percentile(data['charging_score'], 67)
    
    clusters = []
    for _, row in data.iterrows():
        candidates = []
        if row['speed_score'] >= speed_cutoff:
            candidates.append(('speed', row['speed_score']))
        if row['battery_score'] >= battery_cutoff:
            candidates.append(('battery', row['battery_score']))
        if row['charging_score'] >= charging_cutoff:
            candidates.append(('charging', row['charging_score']))
        
        if len(candidates) == 0:
            clusters.append('general')
        else:
            clusters.append(max(candidates, key=lambda x: x[1])[0])
    
    return clusters

def get_top_models_by_cluster(data, cluster_name, score_column, top_n=5):
    """클러스터별 상위 모델 선정"""
    cluster_data = data[data['cluster'] == cluster_name]
    if len(cluster_data) == 0:
        return pd.DataFrame()
    
    return cluster_data.nlargest(min(top_n, len(cluster_data)), score_column)

def generate_web_comment(cluster_name):
    """웹페이지용 코멘트 생성"""
    comments = {
        'speed': {
            'title': '🏎️ 스피드 매니아를 위한 전기차',
            'subtitle': '짜릿한 가속과 최고속도를 자랑하는 퍼포먼스 전기차',
            'description': '드라이빙의 재미와 스포티한 성능을 중시하는 당신을 위해 선별된 전기차들입니다. 강력한 모터와 뛰어난 가속력으로 도로 위의 스릴을 만끽하세요.',
            'target': '스포츠카 애호가, 퍼포먼스 중시 운전자'
        },
        'battery': {
            'title': '🔋 장거리 여행의 최적 파트너',
            'subtitle': '효율성과 주행거리가 뛰어난 실용성 전기차',
            'description': '한 번의 충전으로 더 멀리, 더 경제적으로 이동하고 싶은 당신을 위한 전기차들입니다. 넉넉한 배터리 용량과 뛰어난 에너지 효율로 여행의 자유를 선사합니다.',
            'target': '장거리 통근자, 여행 애호가, 경제성 중시 운전자'
        },
        'charging': {
            'title': '⚡ 빠른 충전의 혁신',
            'subtitle': '급속충전으로 시간을 절약하는 편의성 전기차',
            'description': '바쁜 일상 속에서도 빠른 충전으로 시간을 절약하고 싶은 당신을 위한 전기차들입니다. 최신 급속충전 기술로 짧은 시간에 충분한 에너지를 공급받으세요.',
            'target': '바쁜 직장인, 시간 효율성 중시 운전자'
        }
    }
    return comments.get(cluster_name, {})

def prepare_clustering_data(df):
    """클러스터링을 위한 데이터 준비"""
    features = ['top_speed_kmh', 'acceleration_0_100_s', 'battery_capacity_kWh', 
                'efficiency_wh_per_km', 'range_km', 'fast_charging_power_kw_dc']
    
    # 결측치 제거
    df_clean = df[features + ['brand', 'model']].dropna()
    X = df_clean[features].copy()
    
    # 이상치 클리핑
    for col in X.columns:
        Q1, Q3 = X[col].quantile([0.25, 0.75])
        IQR = Q3 - Q1
        X[col] = X[col].clip(Q1 - 1.5*IQR, Q3 + 1.5*IQR)
    
    # 점수 계산
    speed_scores, battery_scores, charging_scores = calculate_scores(X)
    X['speed_score'] = speed_scores
    X['battery_score'] = battery_scores  
    X['charging_score'] = charging_scores
    
    # 브랜드, 모델 정보 추가
    X['brand'] = df_clean['brand'].values
    X['model'] = df_clean['model'].values
    
    # 클러스터 분류
    X['cluster'] = assign_clusters(X)
    
    return X

def display_recommendation_tab(df):
    """추천 시스템 탭 내용"""
    st.title("🤖 AI 전기차 추천 시스템")
    st.markdown("### 당신의 취향에 맞는 전기차를 찾아보세요!")
    
    # 클러스터링 데이터 준비
    clustered_df = prepare_clustering_data(df)
    
    # 클러스터별 차량 수 통계
    part_counts = clustered_df['cluster'].value_counts()
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🏎️ 속도 특화", f"{part_counts.get('speed', 0)}대")
    with col2:
        st.metric("🔋 배터리 특화", f"{part_counts.get('battery', 0)}대")
    with col3:
        st.metric("⚡ 충전 특화", f"{part_counts.get('charging', 0)}대")
    with col4:
        st.metric("🚗 일반형", f"{part_counts.get('general', 0)}대")
    
    st.markdown("---")
    
    # 클러스터별 추천 표시
    clusters_info = [
        ('speed', 'speed_score', '속도'),
        ('battery', 'battery_score', '배터리'), 
        ('charging', 'charging_score', '충전')
    ]
    
    for cluster_name, score_col, display_name in clusters_info:
        cluster_info = generate_web_comment(cluster_name)
        
        # 클러스터 헤더
        st.markdown(f"## {cluster_info.get('title', f'{display_name} 클러스터')}")
        
        col_info, col_models = st.columns([1, 2])
        
        with col_info:
            st.markdown(f"**{cluster_info.get('subtitle', '')}**")
            st.write(cluster_info.get('description', ''))
            st.info(f"🎯 **추천 대상**: {cluster_info.get('target', '')}")
        
        with col_models:
            top_models = get_top_models_by_cluster(clustered_df, cluster_name, score_col)
            
            if len(top_models) > 0:
                st.markdown(f"**🏆 {display_name} 클러스터 TOP {len(top_models)}**")
                
                for idx, (_, model_data) in enumerate(top_models.iterrows(), 1):
                    with st.expander(f"{idx}. {model_data['brand']} {model_data['model']} ({display_name}점수: {model_data[score_col]:.1f}점)"):
                        col_spec1, col_spec2 = st.columns(2)
                        
                        with col_spec1:
                            if cluster_name == 'speed':
                                st.write(f"🏃 **최고속도**: {model_data['top_speed_kmh']:.0f}km/h")
                                st.write(f"⚡ **제로백**: {model_data['acceleration_0_100_s']:.1f}초")
                            elif cluster_name == 'battery':
                                st.write(f"🔋 **배터리**: {model_data['battery_capacity_kWh']:.1f}kWh")
                                st.write(f"🛣️ **주행거리**: {model_data['range_km']:.0f}km")
                            else:  # charging
                                st.write(f"⚡ **급속충전**: {model_data['fast_charging_power_kw_dc']:.0f}kW")
                                st.write(f"🔋 **배터리**: {model_data['battery_capacity_kWh']:.1f}kWh")
                        
                        with col_spec2:
                            if cluster_name == 'battery':
                                st.write(f"📈 **효율성**: {model_data['efficiency_wh_per_km']:.0f}Wh/km")
                            st.write(f"🏎️ **속도점수**: {model_data['speed_score']:.1f}점")
                            st.write(f"🔋 **배터리점수**: {model_data['battery_score']:.1f}점")
                            st.write(f"⚡ **충전점수**: {model_data['charging_score']:.1f}점")
            else:
                st.warning(f"{display_name} 클러스터에 해당하는 차량이 없습니다.")
        
        st.markdown("---")
    
    # 클러스터별 통계 정보
    with st.expander("📊 클러스터별 상세 통계"):
        stat_col1, stat_col2, stat_col3 = st.columns(3)
        
        with stat_col1:
            if part_counts.get('speed', 0) > 0:
                speed_data = clustered_df[clustered_df['cluster'] == 'speed']
                st.markdown("**🏎️ 속도 클러스터 통계**")
                st.write(f"평균 최고속도: {speed_data['top_speed_kmh'].mean():.1f}km/h")
                st.write(f"평균 제로백: {speed_data['acceleration_0_100_s'].mean():.1f}초")
                st.write(f"평균 속도점수: {speed_data['speed_score'].mean():.1f}점")
        
        with stat_col2:
            if part_counts.get('battery', 0) > 0:
                battery_data = clustered_df[clustered_df['cluster'] == 'battery']
                st.markdown("**🔋 배터리 클러스터 통계**")
                st.write(f"평균 배터리 용량: {battery_data['battery_capacity_kWh'].mean():.1f}kWh")
                st.write(f"평균 주행거리: {battery_data['range_km'].mean():.1f}km")
                st.write(f"평균 효율성: {battery_data['efficiency_wh_per_km'].mean():.1f}Wh/km")
        
        with stat_col3:
            if part_counts.get('charging', 0) > 0:
                charging_data = clustered_df[clustered_df['cluster'] == 'charging']
                st.markdown("**⚡ 충전 클러스터 통계**")
                st.write(f"평균 급속충전: {charging_data['fast_charging_power_kw_dc'].mean():.1f}kW")
                st.write(f"평균 배터리 용량: {charging_data['battery_capacity_kWh'].mean():.1f}kWh")
                st.write(f"평균 충전점수: {charging_data['charging_score'].mean():.1f}점")

def app(df):
    st.set_page_config(layout="wide")  # 전체 화면 폭 사용
    st.title("🔍 나에게 맞는 전기차 찾기")

    hide_streamlit_style = """
        <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        </style>
    """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)

    image = 'log.png'
    col_img, col_title = st.columns([1, 4])
    with col_img:
        st.image(image, width=120)

    # 탭 추가
    tab1, tab2 = st.tabs(["📊 데이터 탐색", "🤖 AI 추천"])
    
    with tab1:
        # 기존 코드 (데이터 탐색 기능)
        eng_to_kor = {
        "brand": "브랜드",
        "model": "모델",
        "top_speed_kmh": "최고 속도 (km/h)",
        "battery_capacity_kWh": "배터리 용량 (kWh)",
        "efficiency_wh_per_km": "효율 (Wh/km)",
        "range_km": "주행 가능 거리 (km)",
        "acceleration_0_100_s": "가속력 (0→100km/h, 초)",
        "fast_charging_power_kw_dc": "급속 충전 전력 (kW, DC)",
        "fast_charge_port": "급속 충전 포트",
        "cargo_volume_l": "적재 용량 (L)",
        "seats": "좌석 수",
        "drivetrain": "구동 방식",
        "car_body_type": "차체 형태",
        "car_size": "차 크기",
        "length_mm": "전장 (mm)",
        "width_mm": "전폭 (mm)",
        "height_mm": "전고 (mm)",
        "torque_nm": "토크 (Nm)",
        "battery_type": "배터리 종류"
        }

        filter_column = ['car_size', 'drivetrain', 'car_body_type']
        car_column = ['brand', 'model']
        hover_column = ["length_mm", "width_mm", "height_mm", "torque_nm", "battery_type", "seats"]
        axis_column = [col for col in df.columns if col not in filter_column + car_column + hover_column]

        def generate_multiselect_filter(df, filter_column) -> list:
            filtered_variable = []
            for filter_element in filter_column:
                options = sorted(df[filter_element].dropna().unique().tolist())
                default_value = [options[0]] if options else []
                selected = st.multiselect(f'{filter_element}', options=options, default=default_value)
                filtered_variable.append((filter_element, selected))
            return filtered_variable

        def return_filtered_df(df: pd.DataFrame, filter_zip: list) -> pd.DataFrame:
            for col, selected_values in filter_zip:
                if selected_values:
                    df = df[df[col].isin(selected_values)]
            return df

        def select_checkbox(axis_column):
            axis_options = ["-- 축을 선택하세요 --"] + axis_column
            x = st.selectbox("X축 변수", axis_options, key="x_axis")
            y_candidates = [col for col in axis_column if col != x]
            y_options = ["-- 축을 선택하세요 --"] + y_candidates
            y = st.selectbox("Y축 변수", y_options, key="y_axis")
            return x, y

        # 🎛️ 대시보드 구조로 레이아웃 나누기
        col_filter, col_control, col_output = st.columns([1.5, 1.2, 3.3])

        with col_filter:
            st.markdown("### 🚗 필터")
            selected_filters = generate_multiselect_filter(df, filter_column)
            filtered_df = return_filtered_df(df, selected_filters)
            st.write("적용된 필터:")
            st.dataframe(filtered_df, use_container_width=True, height=300)

        with col_control:
            st.markdown("### 📊 축 선택")
            if len(filtered_df) > 0 and axis_column:
                x_axis, y_axis = select_checkbox(axis_column)

                st.markdown("### ✅ 브랜드 선택")
                brand_list = sorted(filtered_df["brand"].dropna().unique().tolist())
                selected_brands = []
                for brand in brand_list:
                    if st.checkbox(brand, value=True, key=f"brand_{brand}"):
                        selected_brands.append(brand)

        with col_output:
            st.markdown("### 📈 시각화")
            
            if len(filtered_df) > 0 and axis_column and x_axis and y_axis and x_axis != "-- 축을 선택하세요 --" and y_axis != "-- 축을 선택하세요 --":
                brand_filtered_df = filtered_df[filtered_df["brand"].isin(selected_brands)]

                if len(selected_brands) == 0 or len(brand_filtered_df) == 0:
                    st.warning("선택된 브랜드가 없습니다. 하나 이상 선택해주세요.")

                else:
                    fig = px.scatter(
                        brand_filtered_df,
                        x=x_axis,
                        y=y_axis,
                        color="brand",
                        hover_data=car_column + hover_column
                    )
                    fig.update_traces(
                        marker=dict(size=11)  # 모든 점 크기를 10으로 고정
                    )
                    st.plotly_chart(fig, use_container_width=True)

            else:
                st.info("축과 브랜드를 모두 선택하면 그래프가 표시됩니다.")

        # 히스토그램 (기존 코드 유지)
        if len(filtered_df) > 0 and axis_column and x_axis and x_axis != "-- 축을 선택하세요 --":
            valid_series = filtered_df[x_axis].dropna()
            data_min = valid_series.min()
            data_max = valid_series.max()

            # 예쁜 숫자로 반올림
            rounded_min = np.floor(data_min / 10) * 10
            rounded_max = np.ceil(data_max / 10) * 10

            # 균등한 bin
            n_bins = 10
            bin_edges = np.linspace(rounded_min, rounded_max, n_bins + 1)

            # 안전하게 bin 적용
            filtered_df = filtered_df.dropna(subset=[x_axis])
            filtered_df['bin'] = pd.cut(filtered_df[x_axis], bins=bin_edges, include_lowest=True)
            filtered_df['bin'] = filtered_df['bin'].astype(str)

            # 3. 그룹핑
            grouped = filtered_df.groupby(['bin', 'brand'], observed=True).size().reset_index(name='count')

            # 4. 시각화
            fig2 = px.bar(
                grouped,
                x='bin',
                y='count',
                color='brand',
                title=f'Brand Distribution by {eng_to_kor.get(x_axis, x_axis)}',
                labels={
                    'bin': f"{eng_to_kor.get(x_axis, x_axis)} 구간",
                    'count': '차량 수',
                    'brand': '브랜드'
                }
            )
            fig2.update_layout(
                xaxis_tickangle=-45,
                barmode='stack',
                height=500
            )
            st.plotly_chart(fig2, use_container_width=True)

        if len(filtered_df) > 0 and axis_column and y_axis and y_axis != "-- 축을 선택하세요 --":
            valid_series = filtered_df[y_axis].dropna()
            data_min = valid_series.min()
            data_max = valid_series.max()

            # 예쁜 숫자로 반올림
            rounded_min = np.floor(data_min / 10) * 10
            rounded_max = np.ceil(data_max / 10) * 10

            # 균등한 bin
            n_bins = 10
            bin_edges = np.linspace(rounded_min, rounded_max, n_bins + 1)

            # 안전하게 bin 적용
            filtered_df = filtered_df.dropna(subset=[y_axis])
            filtered_df['bin'] = pd.cut(filtered_df[y_axis], bins=bin_edges, include_lowest=True)
            filtered_df['bin'] = filtered_df['bin'].astype(str)

            # 3. 그룹핑
            grouped = filtered_df.groupby(['bin', 'brand'], observed=True).size().reset_index(name='count')

            # 4. 시각화
            fig3 = px.bar(
                grouped,
                x='bin',
                y='count',
                color='brand',
                title=f'Brand Distribution by {eng_to_kor.get(y_axis, y_axis)}',
                labels={
                    'bin': f"{eng_to_kor.get(y_axis, y_axis)} 구간",
                    'count': '차량 수',
                    'brand': '브랜드'
                }
            )
            fig3.update_layout(
                xaxis_tickangle=-45,
                barmode='stack',
                height=500
            )
            st.plotly_chart(fig3, use_container_width=True)
    
    with tab2:
        # 새로운 추천 시스템 탭
        display_recommendation_tab(df)
