package skitter.auth;

public class User {

    private String username;
    private String RITusername;

    private String firstName;
    private String lastName;
    private String email;

    private boolean isPrivate;
    private int profilePictureID;

    public User() {
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getRITusername() {
        return RITusername;
    }

    public void setRITusername(String RITusername) {
        this.RITusername = RITusername;
    }

    public String getFirstName() {
        return firstName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public boolean isPrivate() {
        return isPrivate;
    }

    public void setPrivate(boolean aPrivate) {
        isPrivate = aPrivate;
    }

    public int getProfilePictureID() {
        return profilePictureID;
    }

    public void setProfilePictureID(int profilePictureID) {
        this.profilePictureID = profilePictureID;
    }
}
