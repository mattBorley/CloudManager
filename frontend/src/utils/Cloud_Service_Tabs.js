const Google = ["Hello", "World"]


export default function GetTabs() {
    const tabs= [
        {
            label: "Google Drive",
            content: Google
        },
        {
            label: "One Drive",
            content: ["TBD"]
        },
        {
            label: "Amazon S3",
            content: ["Third", "Thing", "Here"]
        }
    ];
    if (tabs[0] != null){ return tabs; }
    return null
}