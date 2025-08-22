#!/usr/bin/env python3
"""
Script to retrieve shared links for all files on Dropbox and save them to CSV
"""

import dropbox
import pandas as pd

class DropboxShareLinkExtractor:
    def __init__(self, access_token):
        """
        Initialize Dropbox client
        
        Args:
            access_token (str): Dropbox access token
        """
        self.dbx = dropbox.Dropbox(access_token)
        self.file_links = []
    
    def get_all_files(self, path="", recursive=True):
        """
        Get all files under the specified path
        
        Args:
            path (str): Search start path (default is root)
            recursive (bool): Whether to search recursively
            
        Returns:
            list: List of file information
        """
        try:
            files = []
            result = self.dbx.files_list_folder(path, recursive=recursive)
            
            # Process the first batch
            files.extend([entry for entry in result.entries 
                         if isinstance(entry, dropbox.files.FileMetadata)])
            
            # Continue to get additional batches if available
            while result.has_more:
                result = self.dbx.files_list_folder_continue(result.cursor)
                files.extend([entry for entry in result.entries 
                             if isinstance(entry, dropbox.files.FileMetadata)])
            
            return files
            
        except dropbox.exceptions.ApiError as e:
            return []
    
    def create_shared_link(self, file_path):
        """
        Create or get shared link for the specified file
        
        Args:
            file_path (str): File path
            
        Returns:
            str: Shared link URL (None if unable to retrieve)
        """
        try:
            # Check existing shared links
            try:
                links = self.dbx.sharing_list_shared_links(path=file_path, direct_only=True)
                if links.links:
                    return links.links[0].url
            except dropbox.exceptions.ApiError:
                pass  # No existing links
            
            # Create new shared link
            settings = dropbox.sharing.SharedLinkSettings(
                requested_visibility=dropbox.sharing.RequestedVisibility.public
            )
            link = self.dbx.sharing_create_shared_link_with_settings(file_path, settings)
            return link.url
            
        except dropbox.exceptions.ApiError as e:
            return None
    
    def extract_all_share_links(self, folder_path=""):
        """
        Get shared links for all files
        
        Args:
            folder_path (str): Folder path to search (default is root)
            
        Returns:
            list: List of file information and shared links
        """
        # logger.info("Retrieving file list...")
        files = self.get_all_files(folder_path)
        
        if not files:
            return []
        
        file_data = []
        
        for i, file in enumerate(files, 1):
            
            share_link = self.create_shared_link(file.path_lower)
            
            file_info = {
                'filename': file.name,
                'shared_link': share_link if share_link else 'Link creation failed',
            }
            
            file_data.append(file_info)
            self.file_links.append(file_info)
        
        return file_data
    
    def save_to_csv(self, file_data, output_file="dropbox_share_links.csv"):
        """
        Save file information to CSV
        
        Args:
            file_data (list): List of file information
            output_file (str): Output file name
        """
        try:
            if not file_data:
                return
            
            df = pd.DataFrame(file_data)
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
            
        except Exception as e:
            pass

def main():
    """
    Main function
    """
    # Set Dropbox access token
    # Create an app at https://www.dropbox.com/developers/apps and get the access token
    ACCESS_TOKEN = "sl.u.AF66imnd58dPYU1OpSTQIY8bQ8bSHmp7G6U_TedWLsNdCj3YC6b-rnbOFZlbSUB8J3e8BLUgZs325NZLsfCp-9DE7fyGFKuaFOXQEbjtcQ6vVCYTuBsNGEXcLdcwJBO2LrCwIkGhURSVRFjA2bhIo1m-e-VivhAaeOkMu9dbxC_Bv8iJQ2GxE1L8__dweAFPjhXJfZjDLuCUFmcr5GY4usRBz-JxTBZzlzF2V9oXwpHEBpld_1VVum1INuJpzVNE-__0MlghUMDhHxNT8Jk1uad3RW0H4es6iHu8mzbHXCumvqbJjVVoSqMeGcGfUC7FmZB7g4X1CtjUQyzrHwQHt6StD5UEW741BEcZNnLTQ5uoXS4Ce3ImCiFDWd1qYIYIumKw0ytmHvs-6Fbp9sXrDeQcr1Cp-TXRsr_ETd6UZCjxcikwVSgW9jxKenPKmCztO5YZdDEN0XZeq6FZZxLsV5mboCdwfp5DsSxjAgH_cnUkiAaXJNZUScYfCRDdb1VwKYy_iwfdO-AM_RUJS8yzOA0Dx3Uf9SEK_zHDix2Ggybzow4u0UTIfWsav3wtYa9GNjGZHRA8YrlrddO7O_X1yU8abzEh8wb6qPrIlNlf5dUg4oNaTTbxbGc0RznVr8_M_yZ19j6hu4dJ7hKCUKIZvLTUOOAGpUBP2WnJUtc4Y4I4eeviT-DpBrGXX59tJhZ0y-8NQSWDdeH75fF2g4ynyUk1IgHBRCWbJZ3pnzrB_ooSw96d5XpjFSN_dL30zIJmisfTdKS0HtAepyuE1o87nDhmLAM2NzJxAnrSxou4HTv7YuRsGhlD8o9cTzM5fv2dx9VO4EIrXLeZALCvoj8kdrMpkDbigaQsvjALy7ILpQvMxvldM21TLo3SlphSOfWgG0UOLK54PEGBWFoDz-U6plOYrNShXZbUXu1vcWfj7YrWTwEYjr3gFAF7OBwC0FIyeuR1vjgz-EZjDLeRYWFFbon2eg9tnvvFz7i28adTLUUWkTsaijHc5f7LZutKvV4Kdp4EaVYeqGuvzT7405n6Efyhoo1fQK36Cg7N2kILZqQFaySkmqX9crOTi4jroNaSWiDwfoFV09Mh5x0Mcpv_Fz_VhP_lF5yxInvm51NX2yUKIhOwVAseC4735EjWbzajyngTXrZZxxIGnRHstEmsP6u2vjxB6S_A1GBTmfi4XFh4ovm7uHy3hCCboBlLn1f7poNpQhb5rz89Q0MeC_MKsYPkkk--onA8D7McDQ3klNGuu3hjMcwV5nK2PjbI5vEsP7UYO5Iwl0JmMU-t7ReIEU6O"
    
    # Set output file name
    output_file = "dropbox_share_links.csv"
    
    try:
        # Initialize Dropbox shared link extractor
        extractor = DropboxShareLinkExtractor(ACCESS_TOKEN)
        
        # Specify folder path to search (empty string for root folder)
        folder_path = input("Enter folder path to search (press Enter for root folder): ").strip()
        
        # Get shared links for all files
        file_data = extractor.extract_all_share_links(folder_path)
        
        if file_data:
            # Save to CSV
            extractor.save_to_csv(file_data, output_file)
            
            # Display statistics
            successful_links = len([f for f in file_data if f['shared_link'] != 'Link creation failed'])
            failed_links = len(file_data) - successful_links
            
            print(f"\n=== Processing Results ===")
            print(f"Processed files: {len(file_data)}")
            print(f"Shared link creation successful: {successful_links}")
            print(f"Shared link creation failed: {failed_links}")
            print(f"Output file: {output_file}")
        else:
            pass
            
    except dropbox.exceptions.AuthError:
        print("Authentication error: Access token is invalid")
    except Exception as e:
        print(f"Unexpected error occurred: {e}")

if __name__ == "__main__":
    main()