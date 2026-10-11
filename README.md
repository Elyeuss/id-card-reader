# ID Card Reader

A small web app built with Python and Streamlit. You upload a photo of an ID, and the app uses OCR (EasyOCR) to read the text from it. It shows the original photo next to the extracted text, and can save each scan to Supabase.

Only use sample or fake IDs with this project, never a real one.

## Setup

1. Create a free project at [supabase.com](https://supabase.com).
2. In the SQL Editor, run:

```sql
   create table id_scans (
     id bigint primary key generated always as identity,
     extracted_text text,
     image_path text,
     created_at timestamptz default now()
   );
```

3. In Storage, create a public bucket named `id-images`.
4. Allow uploads to the bucket by running this in the SQL Editor:

```sql
   create policy "anon can upload to id-images"
   on storage.objects for insert
   to anon
   with check (bucket_id = 'id-images');
```

5. Create a `.env` file in the project folder:

```
   SUPABASE_URL=your-project-url
   SUPABASE_KEY=your-publishable-key
```

6. Create a virtual environment and install the packages:

```
   python -m venv venv
   venv\Scripts\activate
   pip install streamlit easyocr python-dotenv supabase pillow
```

EasyOCR downloads its model files the first time it runs. This is normal and only happens once.

## Run

```
venv\Scripts\activate
streamlit run main.py
```

## What I learned

- I learned how programs can read text out of a photo for image scanning and how I can use that for other projects in the future. I learned that these programs can also have misreads with small text and that there are security patterns on the sample license I used for testing (meaning I need to check output to make sure the texts match up). I used AI to build a Streamlit webpage with only Python and no HTML or CSS. Streamlit allowed uploading a file, showing the image, and displaying the text while only taking a line or two to finish.I stored image files in a Supabase Storage with my previous task tracking project files to optimize my free usage. I used a bucket instead of a table as they do different jobs. I learned that Supabase blocks uploads by default and that there is a policy to allow them. I only used a sample ID from Google to keep privacy with IDs. I had a debugging part for the project where FileNotFoundError was just a missing image and the key names in .env had to match the code exactly.