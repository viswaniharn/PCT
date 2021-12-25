# PCT

Collaborator: Bobba Sai Tharak

This was created as part of a hackathon in a former company I have worked. The application is used to detect if a person is susceptible to COVID based on the locations they have visited. If this person visits a place which was visited by a person who has gotten COVID in the past few days(7 days for our use case), then this person is susceptible. This application has features to report themselves as positive to give warnings to others and also mark themselves as recovered. This seggregates the people in different categories based on the time difference of the visits with the people who have COVID. This is used in indoor locations which are most of the office spaces or shopping malls.

This can also be extended to be used as a indoor navigation system. 

This used RNN to get the location of a person based on the signal of the wifi. The location history for 7-10 days of all the people enrolled in the app will be saved to be assessed and classify the person for susceptibility of COVID.
