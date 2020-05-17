use std::io::{Cursor, SeekFrom, Seek, Read, Result, BufRead, Error, ErrorKind};
use byteorder::{LittleEndian, ReadBytesExt};
use encoding_rs::SHIFT_JIS;

/*
from the function caller
lz13::decompress_lz13 -> arc
arc::unpack -> bch files
bch::read -> bch textures
    texture_codec -> return decoded img
bch::parse -> parse decoded bch tex
*/
const HEADER_SIZE : u32 = 0x20;

pub struct File {
    pub filename: String,
    pub bytes: Vec<u8>,
}

struct Header {
    pub file_archive_length: u32,
    pub metadata_ptr_table_offset: u32,
    pub file_count: u32,
    pub is_awakening: bool,  // I have yet to look at awakening's structure
}

struct Metadata {
    pub filename_ptr: u32,
    pub index: u32,
    pub file_length: u32,
    pub file_ptr: u32,
}

// No repacking cause idk how important that would be since the py script exists + no compression yet
pub fn unpack(archive: &[u8]) -> Result<Vec<File>> {
    let mut reader = Cursor::new(archive);
    let header = read_header(&mut reader)?;

    // Initialize array to store files
    let mut files: Vec<File> = Vec::new();
    for count in 0..header.file_count {
        // Get metadata
        let metadata = read_metadata(&header, &mut reader, count)?;

        // Get Filename
        reader.seek(SeekFrom::Start(metadata.filename_ptr as u64))?;
        let mut filename_buffer: Vec<u8> = Vec::new();
        reader.read_until(0x0, &mut filename_buffer)?;
        filename_buffer.pop(); // Don't store the null terminator.
        let (result, _, errors) = SHIFT_JIS.decode(filename_buffer.as_slice());
        if errors {
            return Err(Error::new(ErrorKind::Other, "Failed to decode shift-jis string."))
        }
        let filename = result.into();

        // Get file bytes
        reader.seek(SeekFrom::Start(metadata.file_ptr as u64))?;
        let mut bytes: Vec<u8> = vec![0; metadata.file_length as usize];
        reader.read_exact(&mut bytes)?;

        // Now store the files
        files.push(File { filename, bytes });
    }
    Ok(files)
}

fn read_header(reader: &mut Cursor<&[u8]>) -> Result<Header> {
    let file_archive_length = reader.read_u32::<LittleEndian>()?;
    let metadata_ptr_table_offset = reader.read_u32::<LittleEndian>()? + HEADER_SIZE;
    let file_count = reader.read_u32::<LittleEndian>()?;

    reader.seek(SeekFrom::Start(0x20))?;
    let is_awakening_check= reader.read_u8()?;  // Not really a flag; just that Fates uses a 128 byte-alignment struct
    Ok(Header {
        file_archive_length,
        metadata_ptr_table_offset,
        file_count,
        is_awakening: is_awakening_check != 0,
    })
}

fn read_metadata(header: &Header, reader: &mut Cursor<&[u8]>, count: u32) -> Result<Metadata> {
    reader.seek(SeekFrom::Start((header.metadata_ptr_table_offset + 4 * count) as u64))?;
    let metadata_pointer = reader.read_u32::<LittleEndian>()? + HEADER_SIZE;
    reader.seek(SeekFrom::Start(metadata_pointer as u64))?;

    let filename_ptr = reader.read_u32::<LittleEndian>()? + HEADER_SIZE;
    let index = reader.read_u32::<LittleEndian>()?; // Not necessary
    let file_length = reader.read_u32::<LittleEndian>()?;
    let file_ptr = reader.read_u32::<LittleEndian>()? + 0x80;  // Relative to 128 byte-alignment after header
    Ok(Metadata {
        filename_ptr,
        index,
        file_length,
        file_ptr,
    })
}