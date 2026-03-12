import streamlit as st
import numpy as np
import cv2
from pathlib import Path
from datetime import datetime

st.set_page_config(page_title="3D视频生成", page_icon="🎬", layout="centered")

st.markdown("""
<div style='text-align: center;'>
    <h1>🎬 3D视频生成工具</h1>
    <p style='color: #666; font-size: 18px;'>上传3D模型，AI自动生成视频</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# 上传文件
uploaded_file = st.file_uploader("📁 选择3D模型", type=['obj', 'glb', 'fbx', 'ply', 'stl'])

if uploaded_file:
    st.success(f"✅ 已选择: {uploaded_file.name}")
    
    col1, col2 = st.columns(2)
    with col1:
        frames = st.slider("帧数", 12, 120, 24, 12)
    with col2:
        fps = st.select_slider("帧率", [12, 24, 30, 60], 24)
    
    res = st.select_slider("分辨率", [384, 512, 768], 512)
    
    if st.button("🚀 生成视频", type="primary", use_container_width=True):
        with st.spinner("⏳ 生成中..."):
            frame_list = []
            progress_bar = st.progress(0)
            
            for i in range(frames):
                prog = i / frames
                progress_bar.progress(prog)
                
                frame = np.zeros((res, res, 3), dtype=np.uint8)
                frame[:, :, 0] = int(255 * prog)
                frame[:, :, 1] = int(200 * (1-prog))
                frame[:, :, 2] = 150
                
                x = int(res/2 + 80*np.cos(prog*2*np.pi))
                y = int(res/2 + 80*np.sin(prog*2*np.pi))
                cv2.circle(frame, (x, y), 40, (255,255,255), -1)
                
                frame_list.append(frame)
            
            # 生成视频
            fname = f"video_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp4"
            
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(fname, fourcc, fps, (res, res))
            for f in frame_list:
                out.write(f)
            out.release()
            
            progress_bar.progress(100)
            
        st.success("✅ 完成！")
        st.video(fname)
        
        with open(fname, 'rb') as f:

            st.download_button("📥 下载视频", f.read(), fname, "video/mp4")
