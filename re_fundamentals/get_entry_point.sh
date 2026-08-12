#!/bin/bash

# 1. Parametrin ötürülüb-ötürülmədiyini yoxlayırıq
if [ -z "$1" ]; then
    echo "Error: No file provided."
    exit 1
fi

file_name="$1"

# 2. Faylın mövcudluğunu yoxlayırıq
if [ ! -f "$file_name" ]; then
    echo "Error: File '$file_name' does not exist."
    exit 1
fi

# 3. Faylın ELF formatında olub-olmadığını yoxlayırıq
if ! readelf -h "$file_name" &>/dev/null; then
    echo "Error: '$file_name' is not a valid ELF file."
    exit 1
fi

# 4. readelf vasitəsilə lazımi sahələri çıxarırıq
magic_number=$(readelf -h "$file_name" | grep "Magic:" | sed 's/^[ \t]*Magic:[ \t]*//')
class=$(readelf -h "$file_name" | grep "Class:" | awk '{print $2}')
byte_order=$(readelf -h "$file_name" | grep "Data:" | sed 's/^[ \t]*Data:[ \t]*//')
entry_point_address=$(readelf -h "$file_name" | grep "Entry point address:" | awk '{print $4}')

# 5. messages.sh faylını qoşuruq və funksiyanı çağırırıq
if [ -f "./messages.sh" ]; then
    source ./messages.sh
    display_elf_header_info
else
    echo "ELF Header Information for '$file_name':"
    echo "----------------------------------------"
    echo "Magic Number: $magic_number"
    echo "Class: $class"
    echo "Byte Order: $byte_order"
    echo "Entry Point Address: $entry_point_address"
fi
