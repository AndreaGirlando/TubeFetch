from externalApi.youtube import fromYoutubePlaylistGetLinks


print(fromYoutubePlaylistGetLinks("https://www.youtube.com/playlist?list=PL4fGSI1pDJn6puJdseH2Rt9sMvt9E2M4i").toJson())