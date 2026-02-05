import glob
import cv2 as cv
from pypdf import PdfWriter, PdfReader 
import math
from PIL import Image
import io
import os
import argparse


def add_image_to_pdf(input_pdf_path, output_pdf_path, image_path ):
    # 1. Convert the image to a PDF in memory
    image = Image.open(image_path)
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PDF')
    img_byte_arr.seek(0)

    # 2. Open the image PDF and the existing PDF
    image_pdf = PdfReader(img_byte_arr)
    existing_pdf = PdfReader(input_pdf_path)
    output = PdfWriter()
    # Add the rest of the pages from the original PDF
    for i in range(0, len(existing_pdf.pages)):
        output.add_page(existing_pdf.pages[i])
    output.add_page(image_pdf.pages[0])

    with open(output_pdf_path, "wb") as f:
        output.write(f)

def convert_mp4_to_pngs(path):
    cap = cv.VideoCapture(path)
    frame_number = 0
    os.makedirs('./frames/', exist_ok=True)
    for f in glob.glob("./frames/*"):
        os.remove(f)
    while cap.isOpened():
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        cv.imwrite(f'./frames/frame_{frame_number:03d}.png', frame)
        frame_number += 1
    cap.release()

def main():
    parser = argparse.ArgumentParser('video_to_pdf')
    parser.add_argument('-v','--video', help='Video that will be converted to pdf', required=True)
    parser.add_argument('-o','--output', help='Output pdf name')
    args = parser.parse_args()
    if args.output is None: 
        args.output = 'output.pdf'
    convert_mp4_to_pngs(args.video)

    writer = PdfWriter() 
    page_width = math.floor(8.27 * 72)
    page_height = math.floor(11.69 * 72)

    with open("output.pdf", "wb") as file:
        writer.write(file)
    for frame in os.listdir('./frames'):
        add_image_to_pdf(args.output,args.output,f'./frames/{frame}')

    cv.destroyAllWindows()

main()
