import cv2
import numpy as np
import streamlit as st
from core.config import SIMILARITY_THRESHOLD
from services.embedder.objects_embedder import ObjectsEmbedder
from services.judger.objects_judger import ObjectsJudger


def main():
    st.title("Image Object Difference Detection App")

    # Create a widget to upload image files
    # Display images side by side
    col1, col2 = st.columns(2)

    with col1:
        uploaded_file1 = st.file_uploader("Upload the first jpg", type=["jpg", "jpeg", "png"])

    with col2:
        uploaded_file2 = st.file_uploader("Upload the second jpg", type=["jpg", "jpeg", "png"])

    if uploaded_file1 is not None and uploaded_file2 is not None:
        # Check the extension of the image file and display an error message if it is not in jpg format
        if uploaded_file1.type not in ["image/jpeg", "image/jpg"]:
            st.error("The first image must be in jpg format.")
            return
        if uploaded_file2.type not in ["image/jpeg", "image/jpg"]:
            st.error("The second image must be in jpg format.")
            return

        image1 = cv2.imdecode(np.frombuffer(uploaded_file1.read(), np.uint8), 1)
        image2 = cv2.imdecode(np.frombuffer(uploaded_file2.read(), np.uint8), 1)

        # Display images side by side
        col1, col2 = st.columns(2)

        with col1:
            st.image(image1, channels="BGR", caption="image a", use_column_width=True)

        with col2:
            st.image(image2, channels="BGR", caption="image b", use_column_width=True)

        if st.button("Detect differences between objects"):
            object_embedder = ObjectsEmbedder()
            objects_a = object_embedder.process(image=image1)
            objects_b = object_embedder.process(image=image2)

            # Display images side by side
            col1, col2 = st.columns(2)

            with col1:
                st.subheader("Objects detected in image a")
                for obj_a in objects_a.objects:
                    st.image(obj_a.image, channels="BGR", caption=obj_a.id, use_column_width=True)

            with col2:
                st.subheader("Objects detected in image b")
                for obj_b in objects_b.objects:
                    st.image(obj_b.image, channels="BGR", caption=obj_b.id, use_column_width=True)

            objects_judger = ObjectsJudger(objects_a=objects_a.objects, objects_b=objects_b.objects)
            judgement = objects_judger.process(threshold=SIMILARITY_THRESHOLD)

            # Show differences, if any
            if judgement.has_diff:
                diff_types_str = ", ".join(judgement.diff_types)
                st.write(f"Difference detected.：{diff_types_str}")
            else:
                st.write("No differences were detected.")

            for result in judgement.results:
                if result.is_disappeared:
                    st.write(f"・{result.id_a} has disappeared.")
                if result.id_b_switched:
                    st.write(f"・{result.id_a} and {result.id_b_switched} have been swapped.")
                if result.id_b_matched:
                    st.write(f"・{result.id_a} and {result.id_b_matched} matched.")


if __name__ == "__main__":
    main()
